import jwt
from django.views.decorators.csrf import requires_csrf_token
import json
from datetime import datetime
import bcrypt as bcrypt
import requests
from algosdk import account, mnemonic
from flask import request, jsonify, Blueprint, flash, render_template, current_app, make_response, redirect, url_for
from ..forms.register_form import RegisterForm
from ..forms.login_form import LoginForm

from main.blockchain.algorand import send_algorand_txn, sign_algorand_txn, create_algorand_txn, contract, algod_client
from main.models import User, Transfer, Certificate, Cars
from main.repositories import UserRepository, TransferRepository, CertificateRepository, CarsRepository
from main import db

user = Blueprint('user', __name__)
users = {}
cars = {}
usr_report = UserRepository()
transfer_repo = TransferRepository()
cars_repo = CarsRepository()
cert_repo = CertificateRepository()


@user.route('/register', methods=['POST'])
def register():
    form = RegisterForm()
    if form.validate():
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
    else:
        flash('Usuario no creado, verifique los datos ingresados.', 'danger')
    return render_template('register.html', form=form)

"""
@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        print("VALIDATE")
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            api_url = 'http://localhost:5555/auth/login'
            data = {"email": email, "password": password}
            print("DATA", data)
            headers = {"Content-Type": "application/json", 'X-CSRF-Token': request.cookies['csrf_access_token']}
            response = requests.post(api_url, json=data, headers=headers)
            print("RESPONSE", response.text)

            if response.status_code == 400:
                return render_template('index.html', error="Invalid email or password")

            if response.status_code == 200:
                response = json.loads(response.text)
                token = response["access_token"]
                user_id = str(response["id"])
                resp = make_response(redirect(url_for('home.index')))
                resp.set_cookie('access_token', token)
                resp.set_cookie("id", user_id)
                return resp
            else:
                return render_template('login.html', error="Invalid email or password", form=form)
        else:
            return render_template('login.html', error="Invalid email or password", form=form)
    return render_template('login.html', form=form)

"""


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = {"email": form.email.data, "password": form.password.data}
        print("DATA", data)
        headers = {"content-type": "application/json", 'X-CSRF-Token': request.cookies['csrf_access_token']}
        r = requests.post(
            'http://localhost:5555/login',
            headers=headers,
            data=json.dumps(data))
        if r.status_code == 200:
            print("LO ROMPE EL LOADS")
            user_data = json.loads(r.text)
            print("USER DATA", user_data)
            req = make_response(render_template('profile.html'))
            req.set_cookie('access_token', user_data.get("access_token"), httponly=True)
            return req, 200
        else:
            flash('Usuario o contraseña incorrecta', 'danger')
    return render_template('login.html', form=form)



@user.route('/profile', methods=['GET'])
def profile():
    return render_template('profile.html')


@user.route('/transfer-car', methods=['POST', 'GET'])
def transfer_car():
    data = request.get_json()
    owner = data['owner']
    new_owner = data['new_owner']
    car_id = data['car_id']
    sender = User.query.get(owner)
    recipient = User.query.get(new_owner)
    car_id = Cars.query.get(car_id)

    # Verificar que el remitente sea el propietario actual del automóvil
    if sender.id != car_id.user_id:
        return jsonify({'error': 'El remitente no es el propietario actual del automóvil'}), 400

    # Crear y firmar la transacción de Algorand
    try:
        contr = contract()
        sender_mnemonic = sender.algorand_mnemonic
        algo_txn = create_algorand_txn(sender.algorand_address, recipient.algorand_address)
        signed_txn = sign_algorand_txn(algo_txn, sender_mnemonic)
    except:
        return jsonify({'error': 'No tiene fondos suficientes para realizar la transaccion'}), 400

    # Enviar la transacción de Algorand
    txid = send_algorand_txn(signed_txn)

    cars = Cars(
        user_id=new_owner,
        brand=car_id.brand,
        model=car_id.model,
        year=car_id.year,
    )
    cars_repo.update(cars)
    cars_repo.delete(car_id.id)

    sender = User.query.get(owner)
    recipient = User.query.get(new_owner)
    car = Cars.query.get(car_id)

    # Registrar la transferencia en la base de datos
    transfer = Transfer(
        owner=owner,
        new_owner=new_owner,
        car_id=cars.id,
    )
    transfer_repo.create(transfer)

    # Registrar el certificado de la transferencia en la base de datos
    certificate = Certificate(
        transfer_id=transfer.id,
        owner=owner,
        new_owner=new_owner,
        timestamp=datetime.utcnow(),
        transaction_id_algorand=txid
    )
    db.session.add(certificate)
    db.session.commit()

    return jsonify({'message': 'La transferencia se realizó con éxito'}), 200


@user.route('/mytransfers/<owner>', methods=['GET'])
def get_my_transfers(owner):
    try:
        transfers = transfer_repo.find_by_owner(owner)
        owner = User.query.get(owner)
        trans = owner.to_json()
        new_owner = User.query.get(transfers.new_owner).to_json()
        return jsonify(transfers.to_json(), trans, new_owner), 200
    except AttributeError:
        return jsonify({'Error': 'No tiene transferencias'}), 400


@user.route('/mycars/<user_id>', methods=['GET'])
def get_my_cars(user_id):
    cars = Cars.query.filter_by(user_id=user_id).all()
    return jsonify(cars), 200


@user.route('/mycertificates/<transfer_id>', methods=['GET'])
def get_my_certificates(transfer_id):
    certificates = cert_repo.find_by_id(id=transfer_id)
    owner = User.query.get(certificates.owner).to_json()
    new_owner = User.query.get(certificates.new_owner).to_json()
    return jsonify(certificates.to_json(), owner, new_owner), 200
