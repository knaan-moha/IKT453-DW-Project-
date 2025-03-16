import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
load_dotenv()


mysql_host = os.getenv("MYSQL_HOST")
mysql_user = os.getenv("MYSQL_USER")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_database = os.getenv("MYSQL_DATABASE")
mysql_port = os.getenv("MYSQL_PORT")


def prepare_dw():
    conn = None
    create_db = "CREATE DATABASE IF NOT EXISTS mysql_dw"
    use_dw = "USE mysql_dw"
    
    create_table_dim_product = """
    CREATE TABLE IF NOT EXISTS dim_product(
        Product_Key INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        SKU VARCHAR(255),
        Style VARCHAR(255),
        Category VARCHAR(255),
        Size VARCHAR(255),
        ASIN VARCHAR(255)
    )
    """
    
    try:
        conn = mysql.connector.connect(
            host= mysql_host,
            port  = mysql_port,
            user = mysql_user,
            password = mysql_password
        )
        if conn.is_connected():
            print("Connected to MySQL Server")
            cursor = conn.cursor()
            cursor.execute(create_db)
            cursor.execute(use_dw)
            cursor.execute(create_table_dim_product)
            conn.commit()
            print("Database and tables created successfully")
            
    except Error as e:
        print(e)
    finally: 
        if conn is not None and conn.is_connected():
            conn.close()
            print("Connection closed")
            
if __name__ == '__main__':
    prepare_dw()
    