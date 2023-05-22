from .. import db
from main.repositories import Create, Read, Update
from main.models import Transfer


class TransferRepository(Create, Read, Update):

    def __init__(self):
        self.__transfer = Transfer

    def create(self, model: db.Model) -> Transfer:
        db.session.add(model)
        db.session.commit()
        return model

    def find_all(self):
        return db.session.query(self.__transfer).all()

    def find_by_id(self, id: int) -> Transfer:
        return db.session.query(self.__transfer).get(id)

    def find_by_name(self, name: str) -> Transfer:
        return db.session.query(self.__transfer).filter(self.__transfer.name == name).first()

    def update(self, transfer: Transfer) -> Transfer:
        db.session.add(transfer)
        db.session.commit()
        return transfer

    def delete(self, transfer: Transfer):
        db.session.delete(transfer)
        db.session.commit()
        return transfer
