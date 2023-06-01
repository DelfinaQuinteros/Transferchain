from typing import Dict

from .. import db
from main.repositories import Create, Read, Update
from main.models import Transfer


class TransferRepository(Create, Read, Update):

    def __init__(self):
        self.transfer = Transfer

    def create(self, model: db.Model) -> Transfer:
        db.session.add(model)
        db.session.commit()
        return model

    def find_all(self) -> Dict:
        return db.session.query(self.transfer).all()

    def find_by_id(self, id: int) -> Transfer:
        return db.session.query(self.transfer).get(id)

    def find_by_name(self, name: str) -> Transfer:
        return db.session.query(self.transfer).filter(self.transfer.name == name).first()

    def find_by_recipient_id(self, new_owner: int) -> Transfer:
        return db.session.query(self.transfer).filter(self.transfer.new_owner == new_owner).first()

    def find_by_owner(self, owner: int) -> Transfer:
        return db.session.query(self.transfer).filter(self.transfer.owner == owner).first()

    def update(self, transfer: Transfer) -> Transfer:
        db.session.put(transfer)
        db.session.commit()
        return transfer

    def delete(self, transfer: Transfer):
        db.session.delete(transfer)
        db.session.commit()
        return transfer
