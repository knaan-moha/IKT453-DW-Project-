import pandas as pd 
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import sqlalchemy
import os 
load_dotenv("/Users/zekariamohamed/Vbox_share/IKT453-Dw-Project/.env")

DATABASE = os.getenv("DATABASE")
DB_USER = os.getenv("DB_USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

print(DATABASE, DB_USER, PASSWORD, HOST, PORT)

print(f"mysql+mysqlconnector://{DB_USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

#* loading csv files

amazon_df = pd.read_csv("./Data/Amazon Sale Report.csv")
international_df = pd.read_csv("./Data/International sale Report.csv")
sale_report_df = pd.read_csv("./Data/Sale Report.csv")

#* removing the null values
amazon_df = amazon_df.dropna()
international_df = international_df.dropna()
sale_report_df = sale_report_df.dropna()

print(amazon_df.head())
dim_product = amazon_df[['SKU', 'Style', 'Category', 'Size', 'ASIN']].drop_duplicates()
dim_product = pd.concat([dim_product, international_df[['SKU', 'Style', 'Size']].drop_duplicates()], ignore_index=True)
dim_product = pd.concat([dim_product, sale_report_df[['SKU Code', 'Design No.', 'Category', 'Size']].drop_duplicates()], ignore_index=True)

# Rename columns for consistency
dim_product.rename(columns={'SKU Code': 'SKU', 'Design No.': 'Style'}, inplace=True)

# Add a primary key
dim_product.insert(0, 'Product_Key', range(1, 1 + len(dim_product)))
dim_product = dim_product.loc[:, ~dim_product.columns.duplicated()]

#* connecting to the database
engine = sqlalchemy.create_engine(f"mysql+mysqlconnector://{DB_USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
dim_product.to_sql('dim_product', con=engine, if_exists='append', index=False)
print("Data loaded to MySQL")