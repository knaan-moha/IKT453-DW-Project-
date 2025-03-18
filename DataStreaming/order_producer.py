from kafka import KafkaProducer 
import json 
import time
import os 



producer = KafkaProducer(
    bootstrap_servers= '127.0.0.1:29092', 
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)


order_text_path  = "../DataStreaming/orders.txt"



with open(order_text_path, "r") as file:
    for line in file:
        data = line.strip().split(",")
        order = {
            "order_id": data[0],
            "date_id": int(data[1]),
            "customer_id": int(data[2]),
            "product_id": int(data[3]),
            "fulfillment_id": int(data[4]),
            "promotion_id": int(data[5]),
            "status_id": int(data[6]),
            "courier_status_id": int(data[7]),
            "quantity": int(data[8]),
            "amount": float(data[9]),
            "currency": data[10],
            "B2B": int(data[11]),
            "fulfilled-by": data[12]
        }
        producer.send("order", value=order)
        producer.flush()
        print(f"New order sent: {order}")
        time.sleep(1)

