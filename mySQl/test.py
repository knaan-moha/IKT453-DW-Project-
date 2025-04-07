import pandas as pd
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# CSV file paths (using your existing mapping)
csv_files = {
    "DimCustomer": "./Data/dim_customer.csv",
    "DimDate": "./Data/dim_date.csv",
    "DimProduct": "./Data/dim_product.csv",
    "DimFulfillment": "./Data/dim_fulfillment.csv",
    "DimPromotion": "./Data/dim_promotion.csv",
    "DimOrderStatus": './Data/dim_status.csv',
    "DimCourierStatus": './Data/dim_courier_status.csv',
    "FactSales": './Data/fact_sales.csv'
}

# Neo4j connection details
neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
neo4j_user = os.getenv("NEO4J_USER", "neo4j")
neo4j_password = os.getenv("NEO4J_PASSWORD")



# Connect to Neo4j
driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

def create_constraints(driver):
    """Create constraints in Neo4j for faster lookups and data integrity"""
    constraints = [
        "CREATE CONSTRAINT customer_id IF NOT EXISTS FOR (c:Customer) REQUIRE c.customer_id IS UNIQUE",
        "CREATE CONSTRAINT product_id IF NOT EXISTS FOR (p:Product) REQUIRE p.product_id IS UNIQUE",
        "CREATE CONSTRAINT date_id IF NOT EXISTS FOR (d:Date) REQUIRE d.date_id IS UNIQUE",
        "CREATE CONSTRAINT fulfillment_id IF NOT EXISTS FOR (f:Fulfillment) REQUIRE f.fulfillment_id IS UNIQUE",
        "CREATE CONSTRAINT promotion_id IF NOT EXISTS FOR (p:Promotion) REQUIRE p.promotion_id IS UNIQUE",
        "CREATE CONSTRAINT status_id IF NOT EXISTS FOR (s:OrderStatus) REQUIRE s.status_id IS UNIQUE",
        "CREATE CONSTRAINT courier_status_id IF NOT EXISTS FOR (c:CourierStatus) REQUIRE c.courier_status_id IS UNIQUE",
        "CREATE CONSTRAINT sale_id IF NOT EXISTS FOR (s:Sale) REQUIRE s.sale_id IS UNIQUE"
    ]
    
    with driver.session() as session:
        for constraint in constraints:
            try:
                session.run(constraint)
                print(f"Created constraint: {constraint}")
            except Exception as e:
                print(f"Constraint may already exist: {e}")

def import_dimension_node(driver, csv_path, node_label, id_field):
    """Import a dimension CSV as nodes in Neo4j"""
    try:
        # Read CSV
        df = pd.read_csv(csv_path)
        print(f"Loaded {len(df)} records from {csv_path}")
        
        # Convert to list of dictionaries
        records = df.to_dict('records')
        
        # Process in batches
        batch_size = 1000
        total_records = len(records)
        
        for i in range(0, total_records, batch_size):
            batch = records[i:i+batch_size]
            
            # Cypher query to create nodes
            cypher_query = f"""
            UNWIND $batch AS row
            MERGE (n:{node_label} {{{id_field}: row.{id_field}}})
            SET n += row
            """
            
            with driver.session() as session:
                session.run(cypher_query, batch=batch)
                print(f"Imported batch {i//batch_size + 1}/{(total_records-1)//batch_size + 1} of {node_label}")
        
        print(f"Successfully imported {node_label} nodes")
        
    except Exception as e:
        print(f"Error importing {node_label}: {e}")

def import_fact_sales(driver, csv_path):
    """Import fact sales CSV and create relationships between nodes"""
    try:
        # Read CSV
        df = pd.read_csv(csv_path)
        # Convert column types for proper matching
        df = df.astype({
            "date_id": "int", 
            "customer_id": "int", 
            "product_id": "int",
            "fulfillment_id": "int", 
            "promotion_id": "int", 
            "status_id": "int",
            "courier_status_id": "int"
        }, errors='ignore')
        
        print(f"Loaded {len(df)} records from {csv_path}")
        
        # Add sale_id if not present
        if "sale_id" not in df.columns:
            df["sale_id"] = df.index
        
        # Convert to list of dictionaries
        records = df.to_dict('records')
        
        # Process in batches
        batch_size = 500
        total_records = len(records)
        
        for i in range(0, total_records, batch_size):
            batch = records[i:i+batch_size]
            
            # Cypher query to create sale nodes and relationships
            cypher_query = """
            UNWIND $batch AS row
            
            // Create Sale node
            MERGE (s:Sale {sale_id: row.sale_id})
            SET s += row
            
            // Create relationships to dimension nodes
            WITH s, row
            MATCH (c:Customer {customer_id: row.customer_id})
            MATCH (p:Product {product_id: row.product_id})
            MATCH (d:Date {date_id: row.date_id})
            MATCH (f:Fulfillment {fulfillment_id: row.fulfillment_id})
            MATCH (pr:Promotion {promotion_id: row.promotion_id})
            MATCH (os:OrderStatus {status_id: row.status_id})
            MATCH (cs:CourierStatus {courier_status_id: row.courier_status_id})
            
            MERGE (c)-[:PURCHASED]->(s)
            MERGE (s)-[:CONTAINS]->(p)
            MERGE (s)-[:OCCURRED_ON]->(d)
            MERGE (s)-[:FULFILLED_BY]->(f)
            MERGE (s)-[:APPLIED]->(pr)
            MERGE (s)-[:HAS_STATUS]->(os)
            MERGE (s)-[:HAS_COURIER_STATUS]->(cs)
            """
            
            with driver.session() as session:
                session.run(cypher_query, batch=batch)
                print(f"Imported batch {i//batch_size + 1}/{(total_records-1)//batch_size + 1} of Sales")
        
        print(f"Successfully imported Sales relationships")
        
    except Exception as e:
        print(f"Error importing Sales: {e}")

def main():
    try:
        # Create constraints
        create_constraints(driver)
        
        # Import dimension tables
        dimension_mapping = {
            "DimCustomer": {"label": "Customer", "id_field": "customer_id"},
            "DimDate": {"label": "Date", "id_field": "date_id"},
            "DimProduct": {"label": "Product", "id_field": "product_id"},
            "DimFulfillment": {"label": "Fulfillment", "id_field": "fulfillment_id"},
            "DimPromotion": {"label": "Promotion", "id_field": "promotion_id"},
            "DimOrderStatus": {"label": "OrderStatus", "id_field": "status_id"},
            "DimCourierStatus": {"label": "CourierStatus", "id_field": "courier_status_id"}
        }
        
        for table_name, info in dimension_mapping.items():
            csv_path = csv_files[table_name]
            import_dimension_node(
                driver, 
                csv_path, 
                info["label"], 
                info["id_field"]
            )
        
        # Import fact sales
        import_fact_sales(driver, csv_files["FactSales"])
        
        print("Data import completed successfully")
        
    except Exception as e:
        print(f"Error in main process: {e}")
    finally:
        if 'driver' in locals():
            driver.close()
        print("Process finished")

if __name__ == "__main__":
    main()