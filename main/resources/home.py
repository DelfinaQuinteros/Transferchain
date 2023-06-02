from algosdk import account, mnemonic
from flask import Blueprint, render_template

from main.blockchain.algorand import algod_client

home = Blueprint('home', __name__, template_folder='templates', static_folder='static')


@home.route('/', methods=['GET'])
def index():
    return render_template('register.html')


@home.get("/account")
def create_account():
    private_key, address = account.generate_account()
    passphrase = mnemonic.from_private_key(private_key)

    return {"address": address, "passphrase": passphrase}


@home.get("/account/{Address}")
def get_account_info(Address: str):
    info = algod_client.account_info(Address)
    return {"Address": info}
