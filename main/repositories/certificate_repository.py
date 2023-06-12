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

    def update(self, certificate: Certificate) -> Certificate:
        db.session.add(certificate)
        db.session.commit()
        return certificate

    def get_certificates_user_id(self, user_id: int):
        return db.session.query(self.__certificate).filter(self.__certificate.owner == user_id).all()