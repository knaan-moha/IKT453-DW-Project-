from flask import Flask
from flask_cors import CORS
from my_server.endpoints.analytics_api import analytics_api
from my_server.endpoints.test_api import test_api

app = Flask(__name__)
CORS(app)

# Register the Blueprint correctly
app.register_blueprint(test_api)
app.register_blueprint(analytics_api)

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)
