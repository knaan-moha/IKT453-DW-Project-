from flask import Blueprint, jsonify, request
from my_server.database.query_excuter import fetch_data_from_db
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

analytics_api = Blueprint('analytics_api', __name__)


@analytics_api.route('/analytics', methods=['GET']) 
def get_analytics():
    db_type = request.args.get('DB', 'mysql')
    
    # Get the SQL/Neo4J or query string from URL and params if needed
    query = request.args.get('query')
    params = request.args.getlist('params')  
    # Ensure params are properly converted to appropriate types (int, float, etc.)
    params = [int(param) if param.isdigit() else param for param in params]
    
    # Get collection and filter_query for MongoDB if available
    collection = request.args.get('collection')
    filter_query = request.args.get('filter_query', '{}') 

    print(f"DB Type: {db_type}")
    print(f"Query: {query}")
    print(f"Collection: {collection}")
    print(f"Filter Query: {filter_query}")
    print(f"Params: {params}")

    try:
        # Build the query_params dictionary to pass to fetch_data_from_db
        query_params = {
            "query": query,
            "params": params,
            "collection": collection,
            "filter_query": filter_query
        }

        # Execute the query with extracted parameters
        result = fetch_data_from_db(db_type, query_params)
        return jsonify({"DB": db_type, "query_params": query_params, "result": result})
    except Exception as e:
        analytics_api.logger.error(f"Error fetching analytics: {str(e)}")
        return jsonify({"error": str(e)}), 500

@analytics_api.route('/analytics/mongodb/', methods=['GET'])
def get_all_analytics():
    mongo_uri = os.getenv("MONGO_URI")
    mongo_db = os.getenv("MONGO_DATABASE")
    client = MongoClient(mongo_uri)
    db = client[mongo_db]
    # TODO: fix mongodb endpoint later to be more dynamic

    collection_name = "test"  # Fixed collection name for testing
    data = list(db[collection_name].find({}))  # No filters, returns all documents

    return jsonify({"message": f"Data from MongoDB: {data}"})


