import os
import time
import random
from datetime import datetime, timedelta
import psycopg2
import pandas as pd
from faker import Faker
import schedule
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database connection
DB_CONFIG = {
    'host': 'localhost',
    'database': 'ecommerce',
    'user': 'admin',
    'password': 'password123',
    'port': 5432
}

fake = Faker()

def get_db_connection():
    """Create database connection with retry logic"""
    max_retries = 5
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            return conn
        except psycopg2.OperationalError as e:
            logger.warning(f"DB connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
            else:
                raise

def setup_database():
    """Create tables if they don't exist"""
    logger.info("Setting up database tables...")
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Raw events table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            event_type VARCHAR(50) NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            product_id INTEGER,
            amount DECIMAL(10,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Daily metrics table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS daily_metrics (
            date DATE PRIMARY KEY,
            total_events INTEGER,
            unique_users INTEGER,
            total_revenue DECIMAL(12,2),
            avg_order_value DECIMAL(10,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Product performance table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS product_performance (
            product_id INTEGER,
            date DATE,
            views INTEGER DEFAULT 0,
            purchases INTEGER DEFAULT 0,
            revenue DECIMAL(10,2) DEFAULT 0,
            PRIMARY KEY (product_id, date)
        )
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    logger.info("Database setup complete")

def generate_events(num_events=100):
    """Generate realistic e-commerce events"""
    logger.info(f"Generating {num_events} events...")
    
    events = []
    event_types = ['page_view', 'add_to_cart', 'purchase', 'remove_from_cart']
    
    for _ in range(num_events):
        user_id = random.randint(1, 1000)
        event_type = random.choices(
            event_types, 
            weights=[50, 20, 10, 5]  # page views most common
        )[0]
        
        timestamp = fake.date_time_between(
            start_date='-7d', 
            end_date='now'
        )
        
        product_id = random.randint(1, 100)
        
        # Add amount for purchases
        amount = None
        if event_type == 'purchase':
            amount = round(random.uniform(10, 500), 2)
        
        events.append({
            'user_id': user_id,
            'event_type': event_type,
            'timestamp': timestamp,
            'product_id': product_id,
            'amount': amount
        })
    
    return events

def insert_events(events):
    """Insert events into database"""
    logger.info(f"Inserting {len(events)} events into database...")
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    insert_query = """
        INSERT INTO events (user_id, event_type, timestamp, product_id, amount)
        VALUES (%s, %s, %s, %s, %s)
    """
    
    try:
        for event in events:
            cur.execute(insert_query, (
                event['user_id'],
                event['event_type'],
                event['timestamp'],
                event['product_id'],
                event['amount']
            ))
        
        conn.commit()
        logger.info("Events inserted successfully")
        
    except Exception as e:
        logger.error(f"Error inserting events: {e}")
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

def transform_data():
    """Create aggregated metrics from raw events"""
    logger.info("Running data transformations...")
    
    conn = get_db_connection()
    
    # Update daily metrics
    daily_query = """
        INSERT INTO daily_metrics (date, total_events, unique_users, total_revenue, avg_order_value)
        SELECT 
            DATE(timestamp) as date,
            COUNT(*) as total_events,
            COUNT(DISTINCT user_id) as unique_users,
            COALESCE(SUM(amount), 0) as total_revenue,
            CASE 
                WHEN COUNT(*) FILTER (WHERE event_type = 'purchase') > 0 
                THEN AVG(amount) FILTER (WHERE event_type = 'purchase')
                ELSE 0 
            END as avg_order_value
        FROM events 
        WHERE DATE(timestamp) >= CURRENT_DATE - INTERVAL '7 days'
        GROUP BY DATE(timestamp)
        ON CONFLICT (date) DO UPDATE SET
            total_events = EXCLUDED.total_events,
            unique_users = EXCLUDED.unique_users,
            total_revenue = EXCLUDED.total_revenue,
            avg_order_value = EXCLUDED.avg_order_value,
            created_at = CURRENT_TIMESTAMP
    """
    
    # Update product performance
    product_query = """
        INSERT INTO product_performance (product_id, date, views, purchases, revenue)
        SELECT 
            product_id,
            DATE(timestamp) as date,
            COUNT(*) FILTER (WHERE event_type = 'page_view') as views,
            COUNT(*) FILTER (WHERE event_type = 'purchase') as purchases,
            COALESCE(SUM(amount) FILTER (WHERE event_type = 'purchase'), 0) as revenue
        FROM events 
        WHERE DATE(timestamp) >= CURRENT_DATE - INTERVAL '7 days'
        GROUP BY product_id, DATE(timestamp)
        ON CONFLICT (product_id, date) DO UPDATE SET
            views = EXCLUDED.views,
            purchases = EXCLUDED.purchases,
            revenue = EXCLUDED.revenue
    """
    
    cur = conn.cursor()
    try:
        cur.execute(daily_query)
        cur.execute(product_query)
        conn.commit()
        logger.info("Data transformations completed")
    except Exception as e:
        logger.error(f"Error in transformations: {e}")
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

def run_pipeline():
    """Run the complete data pipeline"""
    logger.info("Starting data pipeline...")
    
    try:
        # Generate and insert events
        events = generate_events(50)  # Smaller batches for demo
        insert_events(events)
        
        # Transform data
        transform_data()
        
        logger.info("Pipeline completed successfully")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise

def check_data_quality():
    """Basic data quality checks"""
    logger.info("Running data quality checks...")
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Check for recent data
    cur.execute("SELECT COUNT(*) FROM events WHERE timestamp >= NOW() - INTERVAL '1 hour'")
    recent_events = cur.fetchone()[0]
    
    # Check for null values
    cur.execute("SELECT COUNT(*) FROM events WHERE user_id IS NULL OR event_type IS NULL")
    null_events = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    
    logger.info(f"Recent events (last hour): {recent_events}")
    logger.info(f"Events with null values: {null_events}")
    
    if null_events > 0:
        logger.warning("Found events with null values!")

def main():
    """Main function to run the data platform"""
    print("Starting Mini Resilient Data Platform")
    print("=" * 50)
    
    try:
        # Setup
        setup_database()
        
        # Initial data load
        logger.info("Running initial data load...")
        events = generate_events(500)  # Initial batch
        insert_events(events)
        transform_data()
        
        # Data quality check
        check_data_quality()
        
        print("\nInitial setup complete!")
        print("Database: http://localhost:5432")
        print("Metabase: http://localhost:3000")
        print("\nTo run continuous pipeline:")
        print("python main.py --continuous")
        
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        return 1
    
    return 0

def continuous_mode():
    """Run pipeline continuously"""
    logger.info("Starting continuous mode...")
    
    # Schedule pipeline to run every 5 minutes
    schedule.every(5).minutes.do(run_pipeline)
    schedule.every(30).minutes.do(check_data_quality)
    
    print("🔄 Continuous pipeline started")
    print("Running every 5 minutes...")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Pipeline stopped by user")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--continuous":
        setup_database()
        continuous_mode()
    else:
        exit_code = main()
        sys.exit(exit_code)
