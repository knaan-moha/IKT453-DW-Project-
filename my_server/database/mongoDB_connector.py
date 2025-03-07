from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class MongoDBConnector:
    def __init__(self):
        # Retrieve environment variables
        self.host = os.getenv('MONGO_HOST')
        self.port = os.getenv('MONGO_PORT')
        self.user = os.getenv('MONGO_USER')
        self.password = os.getenv('MONGO_PASSWORD')
        self.database = os.getenv('MONGO_DATABASE')

        self.client = MongoClient(f'mongodb://{self.user}:{self.password}@{self.host}:{self.port}')
        self.db = self.client[self.database]

    def execute_query(self, collection, filter_query):
        return list(self.db[collection].find(filter_query))

    def close(self):
        self.client.close()
