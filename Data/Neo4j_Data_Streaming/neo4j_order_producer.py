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

# --- Configuration ---
order_csv_path = "../MySQL_Data_Streaming/orders.csv"
watch_path = os.path.dirname(order_csv_path)

# --- MySQL connection ---
mysql_host = os.getenv("MYSQL_HOST")
mysql_user = os.getenv("MYSQL_USER")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_database = os.getenv("MYSQL_DATABASE")
mysql_port = os.getenv("MYSQL_PORT")

conn = mysql.connector.connect(
    port=mysql_port,
    host=mysql_host,
    user=mysql_user,
    password=mysql_password,
    database=mysql_database
)

cursor = conn.cursor()

# --- Kafka producer ---
producer = KafkaProducer(
    bootstrap_servers='127.0.0.1:29092',
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# --- Helper: get latest timestamp from DB ---
def get_last_streamed_timestamp():
    try:
        cursor.execute("SELECT MAX(timestamp) FROM FactSales")
        return cursor.fetchone()[0] or "1970-01-01 00:00:00"
    except mysql.connector.Error as e:
        print(f"⚠️ Warning: Could not get last timestamp from DB: {e}")
        return "1970-01-01 00:00:00"

# --- File watcher handler ---
class OrderFileHandler(FileSystemEventHandler):
    def __init__(self):
        self.timer = None

    def on_modified(self, event):
        if event.src_path.endswith("orders.csv"):
            print("\n📂 Detected changes in orders.csv... resetting timer for 7 seconds.")
            if self.timer:
                self.timer.cancel()
            self.timer = threading.Timer(7, process_new_orders)
            self.timer.start()

# --- Process new rows from CSV ---
last_processed_line = 0
def process_new_orders():
    global last_processed_line

    last_timestamp = get_last_streamed_timestamp()
    print(f"\n🕒 Last timestamp in DB: {last_timestamp}")

    try:
        df = pd.read_csv(order_csv_path)
    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")
        return

    new_orders = df.iloc[last_processed_line:]
    print(f"📄 Found {len(new_orders)} new rows (from line {last_processed_line})")

    order_count = 0
    for index, row in new_orders.iterrows():
        order_timestamp = row.get("timestamp", datetime.now(ZoneInfo("Europe/Oslo")).strftime('%Y-%m-%d %H:%M:%S.%f'))

        if str(order_timestamp) > str(last_timestamp):
            order_count += 1

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

            print(f"\n✅ Produced Order #{order_count}")
            print(f"Order ID:      {order['order_id']}")
            print(f"Customer ID:   {order['customer_id']}")
            print(f"Product ID:    {order['product_id']}")
            print(f"Quantity:      {order['quantity']}")
            print(f"Amount:        {order['amount']} {order['currency']}")
            print(f"Fulfilled by:  {order['fulfilled-by']}")
            print(f"Timestamp:     {order['timestamp']}")
            print("-" * 40)
            time.sleep(1)
        else:
            print("⏩ Skipping row: timestamp not newer than DB.")

    last_processed_line = len(df)
    print("🔁 Done. Watching for new changes in orders.csv...")

# --- Watchdog Observer Setup ---
observer = Observer()
event_handler = OrderFileHandler()
observer.schedule(event_handler, path=watch_path, recursive=False)

print("🚀 Order producer is now watching for changes in orders.csv...")
observer.start()

try:
    while True:
        time.sleep(6)
except KeyboardInterrupt:
    print("\n⏹️  KeyboardInterrupt detected. Stopping observer...")
    observer.stop()
    observer.join()
    print("🛑 Finished watching. Order producer has shut down.")