from flask import Blueprint, jsonify, request

test_api = Blueprint('test_api', __name__)

@test_api.route('/test', methods=['GET'])
def test_connection():
    db_type = request.args.get('db', 'mysql')  # Default to MySQL
    return jsonify({"message": f"Hello {db_type}", "db": db_type})