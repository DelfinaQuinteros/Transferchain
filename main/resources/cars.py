from flask import request, jsonify, Blueprint
from main.models import Cars
from main import db, csrf
from main.repositories import CarsRepository

cars = Blueprint('cars', __name__)
car_repo = CarsRepository()
car = {}


@cars.route('/cars', methods=['POST'])
@csrf.exempt
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





