"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


alumnos = [{

    "name": "Juan",
    "lastname": "Perez",
    "age": 25}]



@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@api.route('/alumnos', methods=['POST'])
def add_alumnos():
    request_body = request.get_json()
    alumnos.append(request_body)
    return jsonify(alumnos), 200

@api.route('/alumnos', methods=['GET'])
def get_alumnos():
    response_body = {
        "alumnos": alumnos
    }
    return jsonify(response_body), 200