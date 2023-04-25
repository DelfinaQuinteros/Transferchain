from .. import db
from main.repositories import Create, Read, Update
from main.models import Certificate


class CertificateRepository(Create, Read, Update):

    def __init__(self):
        self.__certificate = Certificate

    def create(self, model: db.Model) -> Certificate:
        db.session.add(model)
        db.session.commit()
        return model

    def find_all(self):
        return db.session.query(self.__certificate).all()

    def find_by_id(self, id: int) -> Certificate:
        return db.session.query(self.__certificate).get(id)
