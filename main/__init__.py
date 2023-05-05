import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from dotenv import load_dotenv
import pymysql

pymysql.install_as_MySQLdb()

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    load_dotenv()
    # Configuracion de la conexion a la base de datos
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + os.getenv('DATABASE_USER') + ':' + os.getenv(
        'DATABASE_PASSWORD') \
                                            + '@' + os.getenv('DATABASE_URL') + ':' + os.getenv('DATABASE_PORT') \
                                            + '/' + os.getenv('DATABASE_NAME')
    db.init_app(app)
    from main.resources import user, home, cars
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(user, url_prefix='/api/v1')
    app.register_blueprint(cars, url_prefix='/api/v1')
    return app
