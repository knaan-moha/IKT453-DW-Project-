from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Neo4jConnector:
    def __init__(self):
        # Retrieve environment variables
        self.uri = os.getenv('NEO4J_URI')
        self.user = os.getenv('NEO4J_USER')
        self.password = os.getenv('NEO4J_PASSWORD')

        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def execute_query(self, query, params=None):
        with self.driver.session() as session:
            return session.run(query, params or {}).data()

    def close(self):
        self.driver.close()
