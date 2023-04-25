from sqlalchemy import Integer, String, Column

from main import db
from sqlalchemy.ext.hybrid import hybrid_property


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)
    dni = Column(String(20), unique=True, nullable=False)
    email = Column(String(50), nullable=False)
    cars = Column(String(20), nullable=True)
    password = Column(String(128), nullable=False)
    role = Column(String(20), nullable=False, default='client')

    def __repr__(self):
        return f'<User {self.name} {self.last_name} {self.email}>'

