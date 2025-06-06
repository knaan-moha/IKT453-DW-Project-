from flask import Blueprint, jsonify, request
from my_server.database.query_excuter import fetch_data_from_db
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import logging
import traceback
import json

load_dotenv()
logger = logging.getLogger(__name__)
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
        traceback.print_exc()
        logger.error(f"Error fetching analytics: {str(e)}")
        #analytics_api.logger.error(f"Error fetching analytics: {str(e)}")
        return jsonify({"error": str(e)}), 500

@analytics_api.route('/analytics/mongodb/', methods=['GET'])
def get_all_analytics():
    mongo_uri = os.getenv("MONGO_URI")
    mongo_db = os.getenv("MONGO_DATABASE")
    client = MongoClient(mongo_uri)
    db = client[mongo_db]

    collection_name = "fact_sales"
    collection = db[collection_name]

    try:
        pipeline_param = request.args.get('pipeline')
        if not pipeline_param:
            return jsonify({"error": "Missing 'pipeline' query parameter"}), 400

        pipeline = json.loads(pipeline_param)
        if not isinstance(pipeline, list):
            return jsonify({"error": "Pipeline must be a JSON array"}), 400

        result = list(collection.aggregate(pipeline))
        return jsonify({"DB": "mongodb", "collection_name": collection_name, "result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


