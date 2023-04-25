from flask import Blueprint, jsonify

home = Blueprint('home', __name__)


@home.route('/', methods=['GET', 'POST'])
def index():
    return jsonify('Welcome to transferchain'), 200
