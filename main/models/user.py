from sqlalchemy import Integer, String, Column

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

    def __repr__(self):
        return f'<User {self.name} {self.last_name} {self.email}>'

