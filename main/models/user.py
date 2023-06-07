from sqlalchemy import Integer, String, Column
from werkzeug.security import check_password_hash, generate_password_hash

from main import db


class User(db.Model):
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

    # Getter de la contraseña plana no permite leerla
    @property
    def plain_password(self):
        raise AttributeError('Password cant be read')

        # Setter de la contraseña toma un valor en texto plano
        # calcula el hash y lo guarda en el atributo password
    @plain_password.setter
    def plain_password(self, password):
        self.password = generate_password_hash(password)

    def validate_pass(self, password):
        print(f"Password: {password}, Self.password: {self.password}")
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.name} {self.last_name} {self.dni} {self.address}>'

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

