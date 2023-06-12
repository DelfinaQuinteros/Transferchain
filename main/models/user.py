from sqlalchemy import Integer, String, Column
from main import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)
    dni = Column(String(20), unique=True, nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(128), nullable=False)
    algorand_address = Column(String(120), unique=True, nullable=False)
    algorand_mnemonic = Column(String(250), unique=True, nullable=False)
    algorand_private_key = Column(String(250), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.id} {self.name} {self.last_name} {self.dni} {self.address}>'

    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)

    def to_json(self):
        user = {
            'id': self.id,
            'name': self.name,
            'last_name': self.last_name,
            'address': self.address,
            'dni': self.dni,
            'email': self.email
        }
        return user

    def from_json(user):
        id = user['id']
        name = user['name']
        last_name = user['last_name']
        address = user['address']
        dni = user['dni']
        email = user['email']
        return User(
            id=id,
            name=name,
            last_name=last_name,
            address=address,
            dni=dni,
            email=email
        )

