from main import db
from datetime import datetime


def from_json(certificate):
    id = certificate['id']
    transfer_id = certificate['transfer_id']
    recipient_id = certificate['recipient_id']
    sender_id = certificate['sender_id']
    timestamp = certificate['timestamp']
    hash = certificate['hash']
    return Certificate(
        id=id,
        transfer_id=transfer_id,
        recipient_id=recipient_id,
        sender_id=sender_id,
        timestamp=timestamp,
        hash=hash,
    )


class Certificate(db.Model):
    __tablename__ = 'certificate'
    id = db.Column(db.Integer, primary_key=True)
    transfer_id = db.Column(db.Integer, db.ForeignKey('transfers.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    hash = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f"<Certificate {self.id} {self.transfer_id} {self.recipient_id} {self.sender_id} {self.timestamp} {self.hash}>"

    def to_json(self):
        certificate = {
            'id': self.id,
            'transfer_id': self.transfer_id,
            'recipient_id': self.recipient_id,
            'sender_id': self.sender_id,
            'timestamp': self.timestamp,
            'hash': self.hash,
        }
        return certificate
