
from kafka import KafkaConsumer
from dotenv import load_dotenv
from neo4j import GraphDatabase
import json
import os
# Load environment variables
load_dotenv()
# Neo4j connection settings
neo4j_uri = os.getenv("NEO4J_URI")
neo4j_user = os.getenv("NEO4J_USER")
neo4j_password = os.getenv("NEO4J_PASSWORD")
database_name = "neo4j"  # Default Neo4j DB
# Connect to Neo4j
driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
# Kafka Consumer
consumer = KafkaConsumer(
    "order",
    bootstrap_servers='127.0.0.1:29092',
    api_version=(2, 0, 2),
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
)
print("Waiting for new order!")
# Function to insert order into Neo4j
def insert_order_into_neo4j(tx, order):
    query = """
    CREATE (o:Order {
        order_id: $order_id,
        date_id: $date_id,
        customer_id: $customer_id,
        product_id: $product_id,
        fulfillment_id: $fulfillment_id,
        promotion_id: $promotion_id,
        status_id: $status_id,
        courier_status_id: $courier_status_id,
        quantity: $quantity,
        amount: $amount,
        currency: $currency,
        B2B: $B2B,
        fulfilled_by: $fulfilled_by
    })
    """
    tx.run(query, 
        order_id=order["order_id"],
        date_id=order["date_id"],
        customer_id=order["customer_id"],
        product_id=order["product_id"],
        fulfillment_id=order["fulfillment_id"],
        promotion_id=order["promotion_id"],
        status_id=order["status_id"],
        courier_status_id=order["courier_status_id"],
        quantity=order["quantity"],
        amount=order["amount"],
        currency=order["currency"],
        B2B=order["B2B"],
        fulfilled_by=order["fulfilled-by"]
    )
# Main loop
with driver.session(database=database_name) as session:
    for message in consumer:
        order = message.value
        session.execute_write(insert_order_into_neo4j, order)
        print(f"Inserted order into Neo4j: {order['order_id']}")
driver.close()