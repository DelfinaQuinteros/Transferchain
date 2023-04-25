from flask import request, jsonify, Blueprint
import jwt
from werkzeug.security import generate_password_hash, check_password_hash

user = Blueprint('user', __name__)
users = {}


@user.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    role = request.json['role']

    if username in users:
        return jsonify({'error': 'El nombre de usuario ya existe.'}), 409

    password_hash = generate_password_hash(password)

    users[username] = {
        'password': password_hash,
        'role': role
    }

    return jsonify({'message': 'Usuario creado correctamente.'}), 201


@user.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    if username not in users:
        return jsonify({'error': 'Usuario no existe.'}), 401

    if not check_password_hash(users[username]['password'], password):
        return jsonify({'error': 'Contraseña incorrecta.'}), 401

    payload = {
        'username': username,
        'role': users[username]['role']
    }
    token = jwt.encode(payload, user.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({'token': token.decode('utf-8')})
