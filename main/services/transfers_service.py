from main.repositories import TransferRepository
from main.models import Transfer


class TransferService:

    def __init__(self):
        self.repository = TransferRepository()

    def create(self, transfer: Transfer) -> Transfer:
        transfer = self.repository.create(transfer)
        return transfer

    def find_by_id(self, id):
        transfer = self.repository.find_by_id(id)
        return transfer

    def find_all(self):
        transfers = self.repository.find_all()
        return transfers

    def update(self, transfer: Transfer) -> Transfer:
        transfer = self.repository.update(transfer)
        return transfer
