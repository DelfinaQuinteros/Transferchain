import os
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from dotenv import load_dotenv
import pymysql
from flask_wtf.csrf import CSRFProtect

pymysql.install_as_MySQLdb()
db = SQLAlchemy()
csrf = CSRFProtect()
jwt = JWTManager()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'aaaaaaaaaaaaa121321315321'
    load_dotenv()
    login_manager.init_app(app)
    # Configuracion de la conexion a la base de datos
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + os.getenv('DATABASE_USER') + ':' + os.getenv(
        'DATABASE_PASSWORD') \
                                            + '@' + os.getenv('DATABASE_URL') + ':' + os.getenv('DATABASE_PORT') \
                                            + '/' + os.getenv('DATABASE_NAME')
    csrf.init_app(app)
    db.init_app(app)
    from main.resources import user, home, cars
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(user, url_prefix='/')
    app.register_blueprint(cars, url_prefix='/')

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
    jwt.init_app(app)

    return app
