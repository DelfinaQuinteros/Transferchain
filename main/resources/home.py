from algosdk import account, mnemonic
from flask import Blueprint, render_template, flash
from ..forms.login_form import LoginForm
from main.blockchain.algorand import algod_client
from flask import Blueprint, render_template, redirect, url_for, current_app, request, make_response, flash
import requests
import json

home = Blueprint('home', __name__, template_folder='templates', static_folder='static')


@home.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@home.route('/profile')
def profile():
    return render_template('profile.html')


@home.get("/account")
def create_account():
    private_key, address = account.generate_account()
    passphrase = mnemonic.from_private_key(private_key)

    return {"address": address, "passphrase": passphrase}


@home.get("/account/{Address}")
def get_account_info(Address: str):
    info = algod_client.account_info(Address)
    return {"Address": info}
