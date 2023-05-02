import bcrypt as bcrypt
from algosdk import account, transaction
from flask import request, jsonify, Blueprint
import jwt
from pyteal import compileTeal, Mode

from main.__init__ import create_app
from main.models import User, Transfer, Certificate
from main.repositories import UserRepository, TransferRepository, CertificateRepository
from main import db

user = Blueprint('user', __name__)
users = {}
usr_report = UserRepository()
transfer_repo = TransferRepository()


# certificate_repo = CertificateRepository()


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
    # Generar una dirección de Algorand para el nuevo usuario
    new_address = account.generate_account()[1]
    new_user.algorand_address = new_address
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


def get_wallet_address(users_id):
    cursor = db.cursor()
    cursor.execute("SELECT algorand_address FROM users WHERE id=%s", (users_id,))
    result = cursor.fetchone()
    cursor.close()
    if result is None:
        return None
    else:
        return result[0]

