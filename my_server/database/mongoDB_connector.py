import os
from pymongo import MongoClient
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure

# Load environment variables from .env file
load_dotenv()

class MongoDBConnector:
    def __init__(self):
        # Load MongoDB settings from environment variables
        mongo_uri = os.getenv("MONGO_URI")
        mongo_db = os.getenv("MONGO_DATABASE", "my_mongo_database")

        try:
            # Establish connection
            self.client = MongoClient(mongo_uri)
            self.db = self.client[mongo_db]
            # Test connection
            self.client.admin.command('ping')
        except ConnectionFailure as e:
            print(f"MongoDB Connection Error: {e}")
            self.client = None  # Prevent further queries if connection fails

    def execute_query(self, collection_name, query={}):
        if not self.client:
            return {"error": "MongoDB connection is not available"}
        
        # Check if collection exists
        if collection_name not in self.db.list_collection_names():
            return {"error": f"Collection '{collection_name}' does not exist"}

        return list(self.db[collection_name].find(query))

    def close(self):
        if self.client:
            self.client.close()
