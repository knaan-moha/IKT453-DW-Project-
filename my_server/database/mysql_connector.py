import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class MySQLConnector:
    def __init__(self):
        # Retrieve environment variables
        self.host = os.getenv('MYSQL_DW_HOST')
        self.port = os.getenv('MYSQL_DW_PORT')
        self.user = os.getenv('MYSQL_DW_USER')
        self.password = os.getenv('MYSQL_DW_PASSWORD')
        self.database = os.getenv('MYSQL_DW_DATABASE')

        self.conn = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def execute_mysql_query(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()
