from .. import db
from main.repositories import Create, Read, Update
from main.models import User


class UserRepository(Create, Read, Update):

    def __init__(self):
        self.__user = User

    def create(self, model: db.Model) -> User:
        db.session.add(model)
        db.session.commit()
        return model

    def find_all(self):
        return db.session.query(self.__user).all()

    def find_by_id(self, id: int) -> User:
        return db.session.query(self.__user).get(id)

    def find_by_username(self, name: str) -> User:
        return db.session.query(self.__user).filter(self.__user.name == name).first()

    def find_by_email(self, email: str) -> User:
        return db.session.query(self.__user).filter(self.__user.email == email).first()

    def update(self, user: User) -> User:
        db.session.add(user)
        db.session.commit()
        return user
