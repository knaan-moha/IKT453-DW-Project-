from kafka import KafkaConsumer
from neo4j import GraphDatabase
import json
# Kafka consumer setup
consumer = KafkaConsumer(
    "order",
    bootstrap_servers="127.0.0.1:29092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

import pandas as pd
import os
import re
from dotenv import load_dotenv

# Load .env config
load_dotenv()

neo4j_uri = os.getenv("NEO4J_URI")
neo4j_user = os.getenv("NEO4J_USER")
neo4j_password = os.getenv("NEO4J_PASSWORD")
database_name = "neo4j" 
driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

# Kafka consumer setup
consumer = KafkaConsumer(
    "order_Neo4j",
    bootstrap_servers="127.0.0.1:29092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)


def insert_order(tx, order):
    query = """
    MERGE (o:Order {order_id: $order_id})
    SET o.date_id = $date_id,
        o.customer_id = $customer_id,
        o.product_id = $product_id,
        o.fulfillment_id = $fulfillment_id,
        o.promotion_id = $promotion_id,
        o.status_id = $status_id,
        o.courier_status_id = $courier_status_id,
        o.quantity = $quantity,
        o.amount = $amount,
        o.currency = $currency,
        o.B2B = $B2B,
        o.fulfilled_by = $fulfilled_by
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

# Start consuming messages
with driver.session() as session:
    for message in consumer:
        order = message.value
        session.write_transaction(insert_order, order)
        print(f"Inserted order into Neo4j: {order['order_id']}")