from kafka import  KafkaConsumer
from dotenv import load_dotenv
import mysql.connector
import json 
import os
load_dotenv()

mysql_host = os.getenv("MYSQL_DW_HOST")
mysql_user = os.getenv("MYSQL_DW_USER")
mysql_password = os.getenv("MYSQL_DW_PASSWORD") 
mysql_database = os.getenv("MYSQL_DW_DATABASE")
mysql_port = os.getenv("MYSQL_DW_PORT")


conn = mysql.connector.connect(
    port = mysql_port, 
    host = mysql_host, 
    user = mysql_user, 
    password = mysql_password, 
    database = mysql_database
)

cursor = conn.cursor()
insert_count =0
consumer = KafkaConsumer("order",
                        bootstrap_servers='127.0.0.1:29092',
                        api_version=(2,0,2), 
                        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
                        auto_offset_reset='latest', 
                        enable_auto_commit=True,
)

print("Waiting for new order!")
for  message in consumer: 
        order = message.value
        insert_order = """
            INSERT INTO FactSales (order_id, date_id, customer_id, product_id, fulfillment_id, 
                                promotion_id, status_id, courier_status_id, quantity, amount, 
                                currency, B2B, `fulfilled-by`, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
       
    
        values = (
            order["order_id"], order["date_id"], order["customer_id"], order["product_id"], 
            order["fulfillment_id"], order["promotion_id"], order["status_id"], order["courier_status_id"], 
            order["quantity"], order["amount"], order["currency"], order["B2B"], order["fulfilled-by"], order["timestamp"]
        )
    
        cursor.execute(insert_order, values)
        conn.commit()
        insert_count += 1
        print(f"\Received Order: {insert_count}")
        print(f"Order ID: {order['order_id']}")
        print(f"Customer ID: {order['customer_id']}")
        print(f"Product ID: {order['product_id']}")
        print(f"Quantity: {order['quantity']}")
        print(f"Amount: {order['amount']} {order['currency']}")
        print(f"Fulfilled by: {order['fulfilled-by']}")
        print(f"Timestamp: {order['timestamp']}")
        print("-" * 30)

conn.close()
