from typing import Dict, List

from sqlalchemy.orm import aliased, joinedload

from .. import db
from main.repositories import Create, Read, Update
from main.models import Transfer, User, Cars, Certificate


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

    def find_by_owner(self, owner: int) -> List[Transfer]:
        owner_alias = aliased(User)
        new_owner_alias = aliased(User)
        return (
            db.session.query(Transfer)
            .join(owner_alias, owner_alias.id == Transfer.owner)
            .join(new_owner_alias, new_owner_alias.id == Transfer.new_owner)
            .join(Cars)
            .join(Certificate)  # Agrega la relación con el modelo Certificate
            .options(
                joinedload(Transfer.owner_user),
                joinedload(Transfer.new_owner_user),
                joinedload(Certificate.new_owner_user),
                joinedload(Certificate.owner_user)
            )
            .filter(Cars.owner.has(id=owner))
            .all()
        )

    def update(self, transfer: Transfer) -> Transfer:
        db.session.put(transfer)
        db.session.commit()
        return transfer

    def delete(self, transfer: Transfer):
        db.session.delete(transfer)
        db.session.commit()
        return transfer
