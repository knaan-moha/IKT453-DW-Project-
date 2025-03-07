import mysql.connector
from mysql.connector import Error
import sqlalchemy 
def prepare_dw():
    conn = None
    create_db = "CREATE DATABASE IF NOT EXISTS DW"
    use_dw = "USE DW"
    
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
            host='127.0.0.1',
            port  = 23306,
            user = 'deuser', 
            password = 'depassword'
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
    