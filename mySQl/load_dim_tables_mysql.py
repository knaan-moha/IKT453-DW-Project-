import pandas as pd 
import mysql.connector 
from sqlalchemy import create_engine
import os 
from dotenv import load_dotenv

load_dotenv()

mysql_host = os.getenv("MYSQL_HOST")
mysql_user = os.getenv("MYSQL_USER")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_database = os.getenv("MYSQL_DATABASE")
mysql_port = os.getenv("MYSQL_PORT")

engine = create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}")

csv_files = {
    "DimCustomer": "./Data/dim_customer.csv", 
    "DimDate": "./Data/dim_date.csv", 
    "DimProduct": "./Data/dim_product.csv", 
    "DimFulfillment": "./Data/dim_fulfillment.csv", 
    "DimPromotion": "./Data/dim_promotion.csv", 
    "DimOrderStatus": './Data/dim_status.csv',
    "DimCourierStatus":  './Data/dim_courier_status.csv',
    "FactSales": './Data/fact_sales.csv'

    
}
    
for table, file in csv_files.items(): 
    try: 
        df = pd.read_csv(file)
        if table == "FactSales":
            df = df.astype({"date_id": "int", "customer_id": "int", "product_id": "int",
                            "fulfillment_id": "int", "promotion_id": "int", "status_id": "int",
                            "courier_status_id": "int"}, errors='ignore')

        df.to_sql(table, con=engine, if_exists="append", index=False)
        print(f"Loaded csv files in mySql {table}")
    except Exception as e:
        print(f"Error loading: {e}")