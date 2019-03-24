from flask import Flask
from flask import request
from flask_graphql import GraphQLView
import requests
from flask.json import jsonify
from schema import schema
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

@app.route("/")
def hello_world():
    return "Hello World!"

@app.route("/users")
def users():
    response = requests.get('http://localhost:3001/users')
    return jsonify(response.json())


@app.route("/auth/login", methods=['POST'])
def login():
    content = request.json
    print(content)
    response = requests.post('http://localhost:3001/auth/login', json=content)
    return jsonify(response.json())

app.run(port=5000)
