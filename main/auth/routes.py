from cmath import pi
from flask import request, jsonify, Blueprint

from .. import db
from main.models import User
from flask_jwt_extended import create_access_token

# Blueprint para el acceso a los metodos para autenticar
auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login', methods=['POST'])
def login():
    usuario = User.query.filter_by(email=request.get_json().get("email")).first()
    headers = request.headers
    print("ESTA LLEGANDO ACA")
    if usuario.validate_pass(request.get_json().get("password")):
        access_token = create_access_token(identity=usuario)
        data = {
            'id': str(usuario.id),
            'email': usuario.email,
            'access_token': access_token,
        }
        return data, 200
    else:
        return 'Contraseña incorrecta', 401
