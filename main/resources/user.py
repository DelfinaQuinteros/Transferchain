import hashlib
import hmac
import bcrypt as bcrypt
from flask import request, jsonify, Blueprint
import jwt
from main.models import User
from main.repositories import UserRepository

user = Blueprint('user', __name__)
users = {}
usr_report = UserRepository()


@user.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    new_user = User(
        name=data['name'],
        last_name=data['last_name'],
        address=data['address'],
        dni=data['dni'],
        email=data['email'],
        password=hashed_password.decode('utf-8')
    )
    try:
        usr_report.create(new_user)
        return jsonify({'message': 'Usuario creado correctamente.'}), 201
    except:
        return jsonify({'message': 'Error al crear usuario.'}), 500


@user.route('/login', methods=['POST'])
def login():
    user = usr_report.find_by_username(request.json['name'])
    if user:
        if bcrypt.checkpw(request.json['password'].encode('utf-8'), user.password.encode('utf-8')):
            token = jwt.encode({'name': user.name, 'email': user.email, 'role': user.role},
                               'secret_key',
                               algorithm='HS256')
            return jsonify({'token': token}), 200
        else:
            return jsonify({'message': 'Usuario o contraseña incorrectos.'}), 401
    else:
        return jsonify({'message': 'Usuario o contraseña incorrectos.'}), 401


@user.route('/users', methods=['GET'])
def get_users():
    users = usr_report.find_all()
    return jsonify(users), 200


@user.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = usr_report.find_by_id(id)
    return jsonify(user), 200
