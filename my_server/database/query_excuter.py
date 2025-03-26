import json
import os
from dotenv import load_dotenv
from my_server.database.mongoDB_connector import MongoDBConnector
from my_server.database.mysql_connector import MySQLConnector
from my_server.database.neo4j_connector import Neo4jConnector

load_dotenv()

def get_mysql_data(query, params=None):
    mysql_connector = MySQLConnector()
    result = mysql_connector.execute_mysql_query(query, params)
    mysql_connector.close()
    return result


def get_mongo_data(collection, filter_query):
    mongo_connector = MongoDBConnector()
    result = mongo_connector.execute_query(collection, filter_query)
    mongo_connector.close()
    return result


def get_neo4j_data(query, params=None):
    neo4j_connector = Neo4jConnector()
    result = neo4j_connector.execute_query(query, params)
    neo4j_connector.close()
    return result


def fetch_data_from_db(db_type, query_params):
    """
    Fetch data from the respective DB based on db_type.

    :param db_type: Type of DB (mysql, mongo, neo4j)
    :param query_params: Dictionary containing 'query' and 'params'
    :return: Query results or error message
    """
    if db_type == 'mysql':
        query = query_params.get('query')  # Extract query
        params = query_params.get('params', [])  # Extract params

        if isinstance(params, str):
                params = [params]
        return get_mysql_data(query, params)
    elif db_type == 'neo4j':
        query = query_params.get('query')
        params = query_params.get('params', {})
        if isinstance(params, str):
                params = [params]

        # Convert list of params to dictionary {"1": param1, "2": param2, ...}
        param_dict = {str(i + 1): param for i, param in enumerate(params)}
        return get_neo4j_data(query, param_dict)


    elif db_type == 'mongo':
        collection = query_params.get('collection')
        if not collection:
            return {"error": "Collection name is required for MongoDB.", }
        
        filter_query = query_params.get('filter_query', {})
        
        # Ensure filter_query is a valid dictionary
        if isinstance(filter_query, str):
            try:
                filter_query = json.loads(filter_query)  # Parse JSON string if it's in string format
            except Exception as e:
                return {"error": f"Invalid filter_query format: {str(e)}"}
        
        return get_mongo_data(collection, filter_query)


    else:
        return {"error": "Unsupported DB type"}