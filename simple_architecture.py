# simple_architecture.py
# Generate clean, minimal architecture diagram for executive presentations

from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.analytics import Metabase
from diagrams.programming.language import Python
from diagrams.onprem.container import Docker

# Executive-friendly styling - clean and minimal
graph_attr = {
    "fontsize": "20",
    "fontname": "Helvetica Bold",
    "bgcolor": "white",
    "pad": "1.0",
    "rankdir": "LR",
    "splines": "curved",
    "nodesep": "2.0",
    "ranksep": "3.0"
}

node_attr = {
    "fontsize": "14",
    "fontname": "Helvetica Bold",
    "style": "filled,rounded",
    "fillcolor": "#F5F5F5",
    "color": "#333333",
    "penwidth": "3",
    "margin": "0.5,0.3"
}

edge_attr = {
    "fontsize": "12",
    "fontname": "Helvetica",
    "color": "#2196F3",
    "penwidth": "4",
    "arrowsize": "2.0"
}

# Create simple, executive-level diagram
with Diagram("Data Platform - Executive Overview", 
             show=False, 
             direction="LR",
             filename="executive_overview",
             outformat=["png", "svg"],
             graph_attr=graph_attr,
             node_attr=node_attr,
             edge_attr=edge_attr):
    
    # Simple 4-stage pipeline
    data_gen = Python("Data Generation\nPython + Faker\n\n500+ Events/Hour")
    
    data_processing = Python("ETL Pipeline\nValidation & Transform\n\nReal-time Processing")
    
    data_storage = PostgreSQL("PostgreSQL Database\nStructured Storage\n\n3 Optimized Tables")
    
    data_viz = Metabase("Business Intelligence\nInteractive Dashboards\n\nExecutive Insights")
    
    # Infrastructure note
    infrastructure = Docker("Infrastructure\nDocker Compose\n\nFully Containerized")
    
    # Clean data flow
    data_gen >> Edge(label="Raw Events", color="#4CAF50", penwidth="5") >> data_processing
    data_processing >> Edge(label="Clean Data", color="#FF9800", penwidth="5") >> data_storage  
    data_storage >> Edge(label="Analytics", color="#9C27B0", penwidth="5") >> data_viz
    
    # Infrastructure connection (subtle)
    infrastructure >> Edge(label="Orchestrates", color="#757575", style="dashed", penwidth="2") >> data_storage

print("🎯 Executive overview diagram generated!")
print("📁 Perfect for C-level presentations and LinkedIn posts")