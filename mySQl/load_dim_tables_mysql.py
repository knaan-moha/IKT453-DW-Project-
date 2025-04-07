import pandas as pd
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()
load_dotenv(override=True)

# Neo4j credentials from .env
neo4j_uri = os.getenv("NEO4J_URI")  # e.g., "bolt://localhost:7687"
neo4j_user = os.getenv("NEO4J_USER")
neo4j_password = os.getenv("NEO4J_PASSWORD")

# Neo4j driver
driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

# CSV files and table mapping
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

def load_node(tx, label, row):
    query = f"""
    MERGE (n:{label} {{ id: $id }})
    SET n += $props
    """
    tx.run(query, id=row.get('id') or row[list(row.keys())[0]], props=dict(row))

def load_relationship(tx, row):
    query = """
    MATCH (d:DimDate {id: $date_id}),
          (c:DimCustomer {id: $customer_id}),
          (p:DimProduct {id: $product_id}),
          (f:DimFulfillment {id: $fulfillment_id}),
          (pr:DimPromotion {id: $promotion_id}),
          (s:DimOrderStatus {id: $status_id}),
          (cs:DimCourierStatus {id: $courier_status_id})
    MERGE (c)-[r:MADE_ORDER {sales_amount: $sales_amount, quantity: $quantity}]->(p)
    SET r.date_id = $date_id,
        r.fulfillment_id = $fulfillment_id,
        r.promotion_id = $promotion_id,
        r.status_id = $status_id,
        r.courier_status_id = $courier_status_id
    """
    tx.run(query, **row)

# Load data into Neo4j
with driver.session() as session:
    for table, file in csv_files.items():
        try:
            df = pd.read_csv(file)

            # Normalize IDs to 'id' if necessary
            if table != "FactSales":
                for idx, row in df.iterrows():
                    record = row.to_dict()
                    label = table
                    session.write_transaction(load_node, label, record)

            else:
                # Ensure correct types
                df = df.astype({
                    "date_id": "int", "customer_id": "int", "product_id": "int",
                    "fulfillment_id": "int", "promotion_id": "int",
                    "status_id": "int", "courier_status_id": "int"
                }, errors='ignore')

                for idx, row in df.iterrows():
                    record = row.to_dict()
                    session.write_transaction(load_relationship, record)

            print(f"Loaded {table} into Neo4j")

        except Exception as e:
            print(f"Error loading {table}: {e}")
