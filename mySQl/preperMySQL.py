import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
load_dotenv()


mysql_host = os.getenv("MYSQL_DW_HOST")
mysql_user = os.getenv("MYSQL_DW_USER")
mysql_password = os.getenv("MYSQL_DW_PASSWORD")
mysql_database = os.getenv("MYSQL_DW_DATABASE")
mysql_port = os.getenv("MYSQL_DW_PORT")


def prepare_dw():
    conn = None
    create_db = "CREATE DATABASE IF NOT EXISTS mysql_dw_database"
    use_dw = "USE mysql_dw_database"
    
  
    
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
    