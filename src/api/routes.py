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


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users = list(map(lambda x: x.serialize(), users))
    print(users)
    return jsonify(users), 200


@api.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id).serialize()
    print(user)
    return jsonify(user), 200

# Eliminar usuario


@api.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)  # Buscar el usuario por ID

    # Si el usuario no existe, devolver un error
    if not user:
        raise APIException('User not found', status_code=404)

    # Eliminar el usuario
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200

# Crear un nuevo usuario


@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()  # Obtener los datos del cuerpo de la solicitud

    # Validar que los datos necesarios estén presentes
    if not data or 'email' not in data or 'password' not in data:
        raise APIException('Email and password are required', status_code=400)

    # Crear un nuevo usuario
    new_user = User(email=data['email'], password=data['password'], name=data.get(
        'name', ''), is_active=True)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()), 201

# Actualizar un usuario


@api.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)  # Buscar el usuario por ID

    # Si el usuario no existe, devolver un error
    if not user:
        raise APIException('User not found', status_code=404)

    data = request.get_json()  # Obtener los datos del cuerpo de la solicitud

    # Actualizar los campos del usuario si están presentes en los datos
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = data['password']
    if 'name' in data:
        user.name = data['name']
    if 'is_active' in data:
        user.is_active = data['is_active']

    db.session.commit()  # Guardar los cambios en la base de datos

    return jsonify(user.serialize()), 200
