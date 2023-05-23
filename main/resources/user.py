import json
from datetime import datetime
from hashlib import sha256
import bcrypt as bcrypt
from algosdk import account, mnemonic
from flask import request, jsonify, Blueprint
import jwt
from main.blockchain.algorand import send_algorand_txn, sign_algorand_txn, create_algorand_txn, contract
from main.models import User, Transfer, Certificate, Cars
from main.repositories import UserRepository, TransferRepository, CertificateRepository, CarsRepository
from main import db

user = Blueprint('user', __name__)
users = {}
cars = {}
usr_report = UserRepository()
transfer_repo = TransferRepository()
cars_repo = CarsRepository()


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
        password=hashed_password.decode('utf-8'),
    )

    # Generar una dirección, mnemonic key y private key de Algorand para el nuevo usuario
    new_address = account.generate_account()
    new_user.algorand_private_key = new_address[0]
    new_user.algorand_address = new_address[1]
    new_user.algorand_mnemonic = mnemonic.from_private_key(new_address[0])

    usr_report.create(new_user)

    return jsonify({'message': 'Usuario creado correctamente.'}), 201


@user.route('/login', methods=['POST'])
def login():
    user = usr_report.find_by_username(request.json['name'])
    if user:
        if bcrypt.checkpw(request.json['password'].encode('utf-8'), user.password.encode('utf-8')):
            token = jwt.encode({'name': user.name, 'email': user.email},
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


@user.route('/transfer-car', methods=['POST', 'GET'])
def transfer_car():
    data = request.get_json()
    sender_id = data['sender_id']
    recipient_id = data['recipient_id']
    car_id = data['car_id']
    sender = User.query.get(sender_id)
    recipient = User.query.get(recipient_id)
    car_id = Cars.query.get(car_id)

    # Verificar que el remitente sea el propietario actual del automóvil
    if sender.id != car_id.user_id:
        return jsonify({'error': 'El remitente no es el propietario actual del automóvil'}), 400

    # Crear y firmar la transacción de Algorand
    contr = contract()
    sender_mnemonic = sender.algorand_mnemonic
    algo_txn = create_algorand_txn(sender.algorand_address, recipient.algorand_address)
    signed_txn = sign_algorand_txn(algo_txn, sender_mnemonic)

    # Enviar la transacción de Algorand
    txid = send_algorand_txn(signed_txn)

    cars = Cars(
        user_id=recipient_id,
        brand=car_id.brand,
        model=car_id.model,
        year=car_id.year,
    )
    cars_repo.update(cars)
    cars_repo.delete(car_id.id)
    # Registrar la transferencia en la base de datos
    transfer = Transfer(
        sender_id=sender_id,
        recipient_id=recipient_id,
        car_id=cars.id,
    )
    transfer_repo.create(transfer)

    # Registrar el certificado de la transferencia en la base de datos
    certificate = Certificate(
        transfer_id=transfer.id,
        sender_id=sender_id,
        recipient_id=recipient_id,
        timestamp=datetime.utcnow(),
        hash=sha256(str(txid).encode()).hexdigest()
    )
    db.session.add(certificate)
    db.session.commit()

    return jsonify({'message': 'La transferencia se realizó con éxito'}), 200


@user.route('/mytransfers/<sender_id>', methods=['GET'])
def get_my_transfers(sender_id):
    transfers = Transfer.query.filter_by(sender_id=sender_id).all()
    return jsonify(transfers), 200


@user.route('/mycars/<user_id>', methods=['GET'])
def get_my_cars(user_id):
    cars = Cars.query.filter_by(user_id=user_id).all()
    return jsonify(cars), 200


@user.route('/mycertificates/<transfer_id>', methods=['GET'])
def get_my_certificates(transfer_id):
    certificates = Certificate.query.filter_by(transfer_id=transfer_id).all()
    return jsonify(certificates), 200
