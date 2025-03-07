from my_server.database.mongoDB_connector import MongoDBConnector
from my_server.database.mysql_connector import MySQLConnector
from my_server.database.neo4j_connector import Neo4jConnector


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
    :param query_params: Query parameters or query-specific info for each DB
    :return: Query results or error message
    """
    if db_type == 'mysql':
        query = query_params.get('query')
        params = query_params.get('params', [])
        return get_mysql_data(query, params)

    elif db_type == 'mongo':
        collection = query_params.get('collection')
        filter_query = query_params.get('filter_query', {})
        return get_mongo_data(collection, filter_query)

    elif db_type == 'neo4j':
        query = query_params.get('query')
        params = query_params.get('params', {})
        return get_neo4j_data(query, params)

    else:
        return {"error": "Unsupported DB type"}
