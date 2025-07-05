# architecture_diagram_professional.py
# Generate high-quality, enterprise-grade architecture diagram

from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.analytics import Metabase
from diagrams.onprem.compute import Server
from diagrams.onprem.container import Docker
from diagrams.programming.language import Python
from diagrams.onprem.monitoring import Prometheus
from diagrams.aws.storage import S3

# Professional styling attributes
graph_attr = {
    "fontsize": "16",
    "fontname": "Arial",
    "bgcolor": "white",
    "pad": "0.5",
    "rankdir": "TB",
    "splines": "ortho",
    "nodesep": "0.8",
    "ranksep": "1.2"
}

node_attr = {
    "fontsize": "12",
    "fontname": "Arial Bold",
    "style": "rounded,filled",
    "fillcolor": "lightblue",
    "color": "navy",
    "penwidth": "2"
}

edge_attr = {
    "fontsize": "10",
    "fontname": "Arial",
    "color": "darkblue",
    "penwidth": "2",
    "arrowsize": "1.2"
}

# Create the professional architecture diagram
with Diagram("Mini Resilient Data Platform - Architecture Overview", 
             show=False, 
             direction="TB",
             filename="architecture_pro",
             outformat=["png", "svg"],
             graph_attr=graph_attr,
             node_attr=node_attr,
             edge_attr=edge_attr):
    
    # Data Generation Layer
    with Cluster("📊 Data Generation Layer", graph_attr={"style": "filled", "fillcolor": "#E3F2FD"}):
        faker_gen = Python("Faker Library\nRealistic Data Simulation")
        data_gen = Python("Event Generator\n• User Behaviors\n• E-commerce Transactions\n• Real-time Patterns")
        
    # ETL Processing Layer
    with Cluster("⚙️ ETL Processing Layer", graph_attr={"style": "filled", "fillcolor": "#F3E5F5"}):
        pipeline = Server("ETL Pipeline (main.py)\n• Data Ingestion\n• Validation & Quality Checks\n• Error Handling & Retry Logic")
        transform = Server("Data Transformation\n• Business Metrics Calculation\n• Aggregation Engine\n• Performance Optimization")
    
    # Data Storage Layer
    with Cluster("🗄️ Data Storage Layer", graph_attr={"style": "filled", "fillcolor": "#E8F5E8"}):
        db_main = PostgreSQL("PostgreSQL Database")
        with Cluster("Database Tables"):
            events_table = PostgreSQL("events\n(Raw Data)")
            metrics_table = PostgreSQL("daily_metrics\n(Business KPIs)")
            product_table = PostgreSQL("product_performance\n(Analytics)")
    
    # Business Intelligence Layer
    with Cluster("📈 Business Intelligence Layer", graph_attr={"style": "filled", "fillcolor": "#FFF3E0"}):
        dashboard_engine = Metabase("Metabase BI Platform")
        exec_dashboard = Metabase("Executive Dashboard\n• Revenue Analytics\n• User Growth Metrics")
        monitor_dashboard = Metabase("Monitoring Dashboard\n• Pipeline Health\n• Data Quality Status")
    
    # Infrastructure Layer  
    with Cluster("🐳 Infrastructure Layer", graph_attr={"style": "filled", "fillcolor": "#FAFAFA"}):
        orchestration = Docker("Docker Compose\n• Service Orchestration\n• Container Management\n• Environment Isolation")
        monitoring = Prometheus("Monitoring & Logging\n• Pipeline Status\n• Performance Metrics\n• Alert Management")
    
    # Primary Data Flow (Blue arrows - main flow)
    faker_gen >> Edge(label="Generate", color="#1976D2", style="bold") >> data_gen
    data_gen >> Edge(label="Raw Events\n(JSON/CSV)", color="#1976D2", style="bold") >> pipeline
    pipeline >> Edge(label="Validated Data", color="#1976D2", style="bold") >> transform
    transform >> Edge(label="Structured Data", color="#1976D2", style="bold") >> db_main
    
    # Database Internal Flow (Green arrows)
    db_main >> Edge(label="Store", color="#388E3C", style="bold") >> events_table
    db_main >> Edge(label="Aggregate", color="#388E3C", style="bold") >> metrics_table  
    db_main >> Edge(label="Analyze", color="#388E3C", style="bold") >> product_table
    
    # Business Intelligence Flow (Orange arrows)
    events_table >> Edge(label="Query", color="#F57C00", style="bold") >> dashboard_engine
    metrics_table >> Edge(label="Visualize", color="#F57C00", style="bold") >> exec_dashboard
    product_table >> Edge(label="Monitor", color="#F57C00", style="bold") >> monitor_dashboard
    
    # Infrastructure Flow (Gray dashed - management)
    orchestration >> Edge(label="Manages", color="#757575", style="dashed") >> db_main
    orchestration >> Edge(label="Orchestrates", color="#757575", style="dashed") >> dashboard_engine
    pipeline >> Edge(label="Logs", color="#757575", style="dotted") >> monitoring
    transform >> Edge(label="Metrics", color="#757575", style="dotted") >> monitoring

print("✅ Professional architecture diagram generated!")
print("📁 Files created: architecture_pro.png, architecture_pro.svg")