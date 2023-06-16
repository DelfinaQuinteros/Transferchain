from flask_jwt_extended import create_access_token
from flask_login import current_user, login_required, login_user, logout_user, LoginManager
from datetime import datetime
import bcrypt as bcrypt
from algosdk import account, mnemonic
from flask import request, jsonify, Blueprint, render_template, redirect, url_for, flash
from main.blockchain.algorand import send_algorand_txn, sign_algorand_txn, create_algorand_txn, contract, algod_client
from main.forms import LoginForm, TransferForm
from main.models import User, Transfer, Certificate, Cars
from main.repositories import UserRepository, TransferRepository, CertificateRepository, CarsRepository
from main import db, csrf

user = Blueprint('user', __name__)
users = {}
cars = {}
usr_report = UserRepository()
transfer_repo = TransferRepository()
cars_repo = CarsRepository()
cert_repo = CertificateRepository()
login_manager = LoginManager()
login_manager.login_view = 'user.login'


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


@user.route('/login', methods=['GET', 'POST'])
@csrf.exempt
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        if email and password:
            user = usr_report.find_by_email(email)
            if user:
                login_user(user)
                access_token = create_access_token(identity=user.id)
                response = redirect(url_for('user.profile'))
                response.headers['Authorization'] = 'Bearer ' + access_token
                return response
            else:
                return render_template('login.html', error='Usuario o contraseña incorrectos'), flash('Usuario o contraseña incorrectos')
        else:
            return render_template('login.html', error='Usuario o contraseña incorrectos'), flash('Usuario o contraseña incorrectos')

    return render_template('login.html', form=form)



@user.route('/transfer', methods=['POST', 'GET'])
@csrf.exempt
@login_required
def transfer_car():
    form = TransferForm()
    owner_id = User.query.get(current_user.id).id
    print(owner_id)
    print(form.errors)
    print(form.data)
    if form.validate_on_submit():
        print('validado')
        owner = owner_id
        new_owner = form.new_owner.data
        car_id = form.car_id.data
        sender = User.query.get(owner)
        recipient = User.query.get(new_owner)
        car = Cars.query.get(car_id)

        print(sender.id)
        print(car.user_id)
        print(recipient.id)

        # Verificar que el auto exista
        if not car:
            flash('El automóvil no existe', 'danger')

        # Verificar que el nuevo propietario exista
        if not recipient:
            flash('El nuevo propietario no existe', 'danger')

        # Verificar que el remitente sea el propietario actual del automóvil
        if sender.id != car.user_id:
           flash('El remitente no es el propietario actual del automóvil', 'danger')

        # Crear y firmar la transacción de Algorand
        try:
            contr = contract()
            sender_mnemonic = sender.algorand_mnemonic
            algo_txn = create_algorand_txn(sender.algorand_address, recipient.algorand_address)
            signed_txn = sign_algorand_txn(algo_txn, sender_mnemonic)
        except:
            flash('No se pudo crear la transacción de Algorand', 'danger')

        # Enviar la transacción de Algorand
        txid = send_algorand_txn(signed_txn)


        cars = Cars(
                user_id=new_owner,
                brand=car.brand,
                model=car.model,
                year=car.year,
            )
        cars_repo.update(cars)
        cars_repo.delete(car.id)

        transfer = Transfer(
                owner=owner,
                new_owner=new_owner,
                car_id=cars.id,
        )
        transfer_repo.create(transfer)

        certificate = Certificate(
            transfer_id=transfer.id,
            owner=owner,
            new_owner=new_owner,
            timestamp=datetime.utcnow(),
            transaction_id_algorand=txid
        )
        db.session.add(certificate)
        db.session.commit()

        return redirect(url_for('user.profile'))
    return render_template('create_transfer.html', form=form, owner_id=owner_id)



@user.route('/profile')
@login_required
def profile():
    user = User.query.get(current_user.id)
    transfers = Transfer.query.filter((Transfer.owner == user.id) | (Transfer.new_owner == user.id)).all()
    certificates = Certificate.query.filter_by(owner=user.id).all()
    cars = Cars.query.filter(Cars.owner.has(id=user.id)).all()
    return render_template('profile.html', user=user, transfers=transfers, certificates=certificates, cars=cars)

