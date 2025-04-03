# my_server/database/mysql_connector.py
import mysql.connector
from dotenv import load_dotenv
import os
import logging

load_dotenv()
logger = logging.getLogger(__name__)
class MySQLConnector:
    def __init__(self):
        # Print debug information
        host = os.getenv('MYSQL_DW_HOST')
        port = os.getenv('MYSQL_DW_PORT')
        user = os.getenv('MYSQL_DW_USER')
        password = os.getenv('MYSQL_DW_PASSWORD')
        database = os.getenv('MYSQL_DW_DATABASE', os.getenv('MYSQL_DW_DB'))

        print(f"DEBUG - Connecting to MySQL at {host}:{port}, DB: {database}") 
        try:
            
            self.conn = mysql.connector.connect(
                host=host,
                port=int(port),  
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conn.cursor(dictionary=True)
            print(f"Connection established to MySQL at {host}:{port}")
        except Exception as e:
            print(f"Connection error: {str(e)}")
            logger.error(f"MySQL connection error: {str(e)}")
            raise

    def execute_mysql_query(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def close(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
        


