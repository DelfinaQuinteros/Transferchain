from main import db
from datetime import datetime


def from_json(certificate):
    id = certificate['id']
    transfer_id = certificate['transfer_id']
    new_owner = certificate['new_owner']
    owner = certificate['owner']
    timestamp = certificate['timestamp']
    transaction_id_algorand = certificate['transaction_id_algorand']
    return Certificate(
        id=id,
        transfer_id=transfer_id,
        new_owner=new_owner,
        owner=owner,
        timestamp=timestamp,
        transaction_id_algorand=transaction_id_algorand,
    )


class Certificate(db.Model):
    __tablename__ = 'certificate'
    id = db.Column(db.Integer, primary_key=True)
    transfer_id = db.Column(db.Integer, db.ForeignKey('transfers.id'), nullable=False)
    new_owner = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    transaction_id_algorand = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f"<Certificate {self.id} {self.transfer_id} {self.new_owner} {self.owner} {self.timestamp} {self.transaction_id_algorand}>"

    def to_json(self):
        certificate = {
            'id': self.id,
            'transfer_id': self.transfer_id,
            'new_owner': self.new_owner,
            'owner': self.owner,
            'timestamp': self.timestamp,
            'transaction_id_algorand': self.transaction_id_algorand,
        }
        return certificate
