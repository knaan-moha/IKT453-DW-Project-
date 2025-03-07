from flask import Blueprint, jsonify, request
from my_server.database.query_excuter import fetch_data_from_db

analytics_api = Blueprint('analytics_api', __name__)


@analytics_api.route('/analytics', methods=['GET']) 
def get_analytics():
    # Get the DB type from the query string
    db_type = request.args.get('DB', 'mysql')  # Default to MySQL
    print(f"DB Type: {db_type}")

    # Get the request data from the body
    request_body = request.get_json()
    print(f"Request Body: {request_body}")

    if not request_body:
        return jsonify({"error": "Request body must be a valid JSON"}), 400

    if 'query' not in request_body:
        return jsonify({"error": "Query parameter is required in the body"}), 400

    # Ensure params is present in request_body; default to an empty dictionary
    if 'params' not in request_body:
        request_body.setdefault('params', [])

    try:
        # Execute the query based on the db_type and the parameters from the body
        result = fetch_data_from_db(db_type, request_body)
        return jsonify({"DB": db_type, "query": request_body['query'], "result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
