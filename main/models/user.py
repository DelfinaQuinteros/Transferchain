from sqlalchemy import Column, Integer, String

from main import db
from sqlalchemy.ext.hybrid import hybrid_property


class User(db.Model):
    __tablename__ = 'users'

    __id = Column(Integer, primary_key=True)
    __name = Column(String(50), nullable=False)
    __last_name = Column(String(50), nullable=False)
    __address = Column(String(50), nullable=False)
    __dni = Column(String(20), unique=True, nullable=False)
    __email = Column(String(50), nullable=False)
    __cars = Column(String(20), nullable=True)
    __password = Column(String(128), nullable=False)
    __role = Column(String(20), nullable=False, default='client')

    def __repr__(self):
        return f'<User {self.__id} {self.__name} {self.__last_name} {self.__email} {self.__address} {self.__role} ' \
               f'{self.__cars}>'

    def __init__(self, role, password, email, dni, address, last_name, name, id, cars):
        self.__car = cars
        self.__role = role
        self.__password = password
        self.__email = email
        self.__dni = dni
        self.__address = address
        self.__last_name = last_name
        self.__name = name
        self.__id = id

    @hybrid_property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @id.deleter
    def id(self):
        del self.__id

    @hybrid_property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @name.deleter
    def name(self):
        del self.__name

    @hybrid_property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, last_name):
        self.__last_name = last_name

    @last_name.deleter
    def last_name(self):
        del self.__last_name
        
    @hybrid_property
    def address(self):
        return self.__address

    @address.setter
    def address(self, address):
        self.__address = address

    @address.deleter
    def address(self):
        del self.__address
        
    @hybrid_property
    def dni(self):
        return self.__dni

    @dni.setter
    def dni(self, dni):
        self.__dni = dni

    @dni.deleter
    def dni(self):
        del self.__dni
    
    @hybrid_property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    @email.deleter
    def email(self):
        del self.__email
        
    @hybrid_property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password

    @password.deleter
    def password(self):
        del self.__password

    @hybrid_property
    def role(self):
        return self.__role

    @role.setter
    def role(self, role):
        self.__role = role

    @role.deleter
    def role(self):
        del self.__role

    @hybrid_property
    def cars(self):
        return self.__cars

    @cars.setter
    def cars(self, cars):
        self.__cars = cars

    @cars.deleter
    def cars(self):
        del self.__cars
