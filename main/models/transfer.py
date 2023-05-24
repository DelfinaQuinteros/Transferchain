from datetime import datetime
from main import db


def from_json(transfers):
    id = transfers['id']
    date = transfers['date']
    sender_id = transfers['sender_id']
    recipient_id = transfers['recipient_id']
    car_id = transfers['car_id']
    return Transfer(
        id=id,
        date=date,
        sender_id=sender_id,
        recipient_id=recipient_id,
        car_id=car_id,

    )


class Transfer(db.Model):
    __tablename__ = 'transfers'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)

    def __repr__(self):
        return f"<Transferencia {self.id} {self.date} {self.sender_id} {self.recipient_id}>"

    def to_json(self):
        transfers = {
            'id': self.id,
            'date': self.date,
            'sender_id': self.sender_id,
            'recipient_id': self.recipient_id,
            'car_id': self.car_id,
        }
        return transfers
