from kafka import KafkaProducer 
import json 
import time
import os 
import threading
import mysql.connector
from zoneinfo import ZoneInfo
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd

mysql_host = os.getenv("MYSQL_HOST")
mysql_user = os.getenv("MYSQL_USER")
mysql_password = os.getenv("MYSQL_PASSWORD") 
mysql_database = os.getenv("MYSQL_DATABASE")
mysql_port = os.getenv("MYSQL_PORT")

conn = mysql.connector.connect(
    port = mysql_port, 
    host = mysql_host, 
    user = mysql_user, 
    password = mysql_password, 
    database = mysql_database
)

cursor = conn.cursor()

producer = KafkaProducer(
    bootstrap_servers= '127.0.0.1:29092', 
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

order_csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../MySQL_Data_Streaming/orders.csv")



#* function for retrieve the last

def get_last_streamed_timestamp():
    cursor.execute("SELECT MAX(timestamp) FROM FactSales")
    last_timestamp = cursor.fetchone()[0]
    return last_timestamp

#print(get_last_streamed_timestamp())
class OrderFileHandler(FileSystemEventHandler): 
    def __init__(self):
        self.timer = None

    def on_modified(self, event):
        if event.src_path.endswith("orders.csv"):
            print("Detected changes in orders.csv... resetting timer for 7 seconds.")
            #*NOTE here just tried for 7 second we can change it letter to 5 min or more!

            if self.timer:
                self.timer.cancel()  # Cancel any existing timer

            self.timer = threading.Timer(7, process_new_orders)  # Start a new 7-sec timer
            self.timer.start()
last_processed_line = 0
def process_new_orders():
    
    last_timestamp = get_last_streamed_timestamp()
    global last_processed_line
    
    try: 
        df = pd.read_csv(order_csv_path)
    except Exception as e:
        print(f"Error reading csv file {e}")
        return 
    
    new_orders = df.iloc[last_processed_line:]
    order_count = 0
    for index, row in new_orders.iterrows(): 
        order_timestamp = row.get("timestamp", datetime.now(ZoneInfo("Europe/Oslo")).strftime('%Y-%m-%d %H:%M:%S.%f'))
        if order_timestamp > last_timestamp:
                order_count +=1
              
                order = {
                    "order_id": row["order_id"],
                    "date_id": int(row["date_id"]),
                    "customer_id": int(row["customer_id"]),
                    "product_id": int(row["product_id"]),
                    "fulfillment_id": int(row["fulfillment_id"]),
                    "promotion_id": int(row["promotion_id"]),
                    "status_id": int(row["status_id"]),
                    "courier_status_id": int(row["courier_status_id"]),
                    "quantity": int(row["quantity"]),
                    "amount": float(row["amount"]),
                    "currency": row["currency"],
                    "B2B": int(row["B2B"]),
                    "fulfilled-by": row["fulfilled-by"],
                    "timestamp": order_timestamp
                }
                producer.send("order", value=order)
                producer.flush()
                print(f"\nProduced Order: {order_count}")
                print(f"Order ID: {order['order_id']}")
                print(f"Customer ID: {order['customer_id']}")
                print(f"Product ID: {order['product_id']}")
                print(f"Quantity: {order['quantity']}")
                print(f"Amount: {order['amount']} {order['currency']}")
                print(f"Fulfilled by: {order['fulfilled-by']}")
                print(f"Timestamp: {order['timestamp']}")
                print("-" * 30)  # Separator for readability
                time.sleep(1)
        last_processed_line = len(df)
        print("Order producer is now watching for changes in order.csv...")
#* watchdog observer for monitoring the file changes continuously 
observer = Observer()
event_handler = OrderFileHandler()
observer.schedule(event_handler, path="", recursive=False)
print("Order producer is now watching for changes in order.csv...")
observer.start()

try:
    while True:
        time.sleep(1)  
except KeyboardInterrupt:
    observer.stop()

observer.join()