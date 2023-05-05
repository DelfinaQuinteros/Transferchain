from algokit_utils import account
from algosdk import transaction
from flask import request, jsonify, Blueprint
from pyteal import compileTeal, Mode

from main.models import Cars
from main import db
from algosdk.v2client import algod, indexer
from main.repositories import CarsRepository

cars = Blueprint('cars', __name__)
car_repo = CarsRepository()
car = {}


@cars.route('/cars', methods=['POST'])
def create_car():
    global car
    car = request.get_json()
    new_car = Cars(
        brand=car['brand'],
        model=car['model'],
        year=car['year'],
        user_id=car['user_id']
    )
    car_repo.create(new_car)
    return jsonify({'message': 'Car created: ' + car['brand']}), 201


algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "TnqYtzsJKK1DS3TLNWDJ29wZEex8Y3iy5kNjhrx6"
headers = {
    "X-API-Key": algod_token,
}
algod_client = algod.AlgodClient(algod_token, algod_address, headers)

indexer_address = "https://testnet-algorand.api.purestake.io/idx2"
indexer_token = ""
indexer_client = indexer.IndexerClient(indexer_token, indexer_address, headers)




