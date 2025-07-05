# data_flow_diagram_professional.py
# Generate enterprise-quality data flow diagram

from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.analytics import Metabase
from diagrams.onprem.compute import Server
from diagrams.programming.language import Python
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.queue import Kafka
from diagrams.onprem.network import Internet

# High-quality styling for enterprise presentation
graph_attr = {
    "fontsize": "18",
    "fontname": "Helvetica Bold",
    "bgcolor": "#FAFAFA",
    "pad": "1.0",
    "rankdir": "LR", 
    "splines": "ortho",
    "nodesep": "1.0",
    "ranksep": "2.0",
    "concentrate": "true"
}

node_attr = {
    "fontsize": "11",
    "fontname": "Helvetica",
    "style": "rounded,filled",
    "fillcolor": "#FFFFFF",
    "color": "#2E7D32",
    "penwidth": "2.5",
    "margin": "0.3"
}

edge_attr = {
    "fontsize": "9",
    "fontname": "Helvetica",
    "color": "#1565C0",
    "penwidth": "2.5",
    "arrowsize": "1.5",
    "arrowhead": "vee"
}

# Create detailed data flow diagram
with Diagram("Data Platform - Enterprise Data Flow Architecture", 
             show=False, 
             direction="LR",
             filename="data_flow_enterprise",
             outformat=["png", "svg"],
             graph_attr=graph_attr,
             node_attr=node_attr,
             edge_attr=edge_attr):
    
    # Input Sources
    with Cluster("🎯 Data Sources", graph_attr={"style": "filled", "fillcolor": "#E1F5FE", "color": "#0277BD"}):
        user_sim = Internet("User Simulation\nBehavior Patterns")
        faker_lib = Python("Faker Library\nData Generation")
        event_types = Server("Event Types\n• Page Views\n• Add to Cart\n• Purchases\n• User Actions")
    
    # Data Ingestion Pipeline
    with Cluster("🔄 Ingestion Pipeline", graph_attr={"style": "filled", "fillcolor": "#F3E5F5", "color": "#7B1FA2"}):
        data_collector = Python("Data Collector\nmain.py")
        validator = Server("Data Validator\n• Schema Validation\n• Quality Checks\n• Error Detection")
        error_handler = Server("Error Handler\n• Retry Logic\n• Dead Letter Queue\n• Alert System")
    
    # Processing Engine  
    with Cluster("⚡ Processing Engine", graph_attr={"style": "filled", "fillcolor": "#E8F5E8", "color": "#2E7D32"}):
        etl_engine = Python("ETL Engine\nTransformation Logic")
        aggregator = Server("Aggregation Service\n• Daily Metrics\n• Product Performance\n• User Analytics")
        scheduler = Kafka("Task Scheduler\nBatch Processing")
    
    # Data Warehouse
    with Cluster("🏗️ Data Warehouse", graph_attr={"style": "filled", "fillcolor": "#FFF3E0", "color": "#F57C00"}):
        postgres_main = PostgreSQL("PostgreSQL 15\nCore Database")
        
        with Cluster("Table Schema"):
            raw_events = PostgreSQL("events\n• user_id\n• event_type\n• timestamp\n• product_id\n• amount")
            daily_agg = PostgreSQL("daily_metrics\n• date\n• total_revenue\n• unique_users\n• avg_order_value")
            product_perf = PostgreSQL("product_performance\n• product_id\n• views\n• purchases\n• conversion_rate")
    
    # Analytics & BI Layer
    with Cluster("📊 Analytics & BI", graph_attr={"style": "filled", "fillcolor": "#E8EAF6", "color": "#3F51B5"}):
        metabase_engine = Metabase("Metabase Engine\nQuery Processor")
        
        with Cluster("Dashboard Suite"):
            exec_kpis = Metabase("Executive KPIs\n• $30.2K Revenue\n• 19.14% Conversion\n• 949 Users")
            realtime_monitor = Metabase("Real-time Monitor\n• Pipeline Health\n• Data Quality\n• System Status")
            product_analytics = Metabase("Product Analytics\n• Top Products\n• Performance Trends\n• User Behavior")
    
    # Monitoring & Observability
    with Cluster("🔍 Observability", graph_attr={"style": "filled", "fillcolor": "#FFEBEE", "color": "#C62828"}):
        log_aggregator = Prometheus("Log Aggregator\nCentralized Logging")
        health_monitor = Server("Health Monitor\n• Pipeline Status\n• Data Freshness\n• Error Rates")
        alerting = Server("Alert Manager\n• Threshold Monitoring\n• Notification System\n• SLA Tracking")
    
    # PRIMARY DATA FLOW (Thick blue arrows)
    user_sim >> Edge(label="Simulates", color="#0D47A1", style="bold", penwidth="3") >> faker_lib
    faker_lib >> Edge(label="Generates", color="#0D47A1", style="bold", penwidth="3") >> event_types
    event_types >> Edge(label="Raw Events\n(1K+ events/hour)", color="#0D47A1", style="bold", penwidth="3") >> data_collector
    
    # VALIDATION FLOW (Green arrows)
    data_collector >> Edge(label="Validate", color="#1B5E20", style="bold", penwidth="2.5") >> validator
    validator >> Edge(label="Clean Data", color="#1B5E20", style="bold", penwidth="2.5") >> etl_engine
    validator >> Edge(label="Errors", color="#D32F2F", style="dashed") >> error_handler
    
    # PROCESSING FLOW (Purple arrows) 
    etl_engine >> Edge(label="Process", color="#4A148C", style="bold", penwidth="2.5") >> aggregator
    aggregator >> Edge(label="Schedule", color="#4A148C", style="bold", penwidth="2.5") >> scheduler
    scheduler >> Edge(label="Batch Insert", color="#4A148C", style="bold", penwidth="2.5") >> postgres_main
    
    # DATABASE STORAGE (Orange arrows)
    postgres_main >> Edge(label="Raw Storage", color="#E65100", penwidth="2") >> raw_events
    postgres_main >> Edge(label="Aggregated", color="#E65100", penwidth="2") >> daily_agg
    postgres_main >> Edge(label="Analytics", color="#E65100", penwidth="2") >> product_perf
    
    # ANALYTICS QUERIES (Blue arrows)
    raw_events >> Edge(label="Query", color="#1565C0", penwidth="2") >> metabase_engine
    daily_agg >> Edge(label="Visualize", color="#1565C0", penwidth="2") >> exec_kpis
    product_perf >> Edge(label="Analyze", color="#1565C0", penwidth="2") >> product_analytics
    postgres_main >> Edge(label="Monitor", color="#1565C0", penwidth="2") >> realtime_monitor
    
    # MONITORING FLOWS (Red dotted lines)
    data_collector >> Edge(label="Logs", color="#B71C1C", style="dotted") >> log_aggregator
    validator >> Edge(label="Quality Metrics", color="#B71C1C", style="dotted") >> health_monitor
    etl_engine >> Edge(label="Performance", color="#B71C1C", style="dotted") >> health_monitor
    health_monitor >> Edge(label="Alerts", color="#B71C1C", style="dashed") >> alerting

print("🎨 Enterprise data flow diagram generated!")
print("📁 Files created: data_flow_enterprise.png, data_flow_enterprise.svg")
print("💡 High-resolution SVG version available for presentations!")