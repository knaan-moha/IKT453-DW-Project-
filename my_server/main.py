from flask import Flask, jsonify
import os
from flask_cors import CORS
from my_server.endpoints.analytics_api import analytics_api
from my_server.endpoints.test_api import test_api

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Register the Blueprint correctly
app.register_blueprint(test_api)
app.register_blueprint(analytics_api)

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/debug-env')
def debug_env():
    return jsonify({
        'mysql_host': os.getenv('MYSQL_DW_HOST'),
        'mysql_port': os.getenv('MYSQL_DW_PORT')
    })

if __name__ == '__main__':
    #app.run(debug=True)
    print(f"Using MySQL host: {os.getenv('MYSQL_DW_HOST')}, port: {os.getenv('MYSQL_DW_PORT')}")
    app.run(host="0.0.0.0", port=5000)
