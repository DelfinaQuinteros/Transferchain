import os
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request
from dotenv import load_dotenv
import pymysql
from flask_wtf.csrf import CSRFProtect

pymysql.install_as_MySQLdb()
csrf = CSRFProtect()
db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config['API_URL'] = 'http://localhost:5555'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    csrf.init_app(app)
    # Configuracion de la conexion a la base de datos
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + os.getenv('DATABASE_USER') + ':' + os.getenv(
        'DATABASE_PASSWORD') \
                                            + '@' + os.getenv('DATABASE_URL') + ':' + os.getenv('DATABASE_PORT') \
                                            + '/' + os.getenv('DATABASE_NAME')
    db.init_app(app)
    from main.resources import user, home, cars
    from main.auth import auth
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(user, url_prefix='/')
    app.register_blueprint(cars, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    return app
