from typing import Dict

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

    def find_all(self) -> Dict:
        return db.session.query(self.__transfer).all()

    def find_by_id(self, id: int) -> Transfer:
        return db.session.query(self.__transfer).get(id)

    def find_by_name(self, name: str) -> Transfer:
        return db.session.query(self.__transfer).filter(self.__transfer.name == name).first()

    def find_by_user_id(self, user_id: int) -> Transfer:
        return db.session.query(self.__transfer).filter(self.__transfer.user_id == user_id).first()

    def find_by_sender_id(self, sender_id: int) -> Transfer:
        return db.session.query(self.__transfer).filter(self.__transfer.sender_id == sender_id).first()

    def update(self, transfer: Transfer) -> Transfer:
        db.session.put(transfer)
        db.session.commit()
        return transfer

    def delete(self, transfer: Transfer):
        db.session.delete(transfer)
        db.session.commit()
        return transfer
