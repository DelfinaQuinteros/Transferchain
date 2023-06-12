from datetime import datetime
from main import db


def from_json(transfers):
    id = transfers['id']
    date = transfers['date']
    owner = transfers['owner']
    new_owner = transfers['new_owner']
    car_id = transfers['car_id']
    return Transfer(
        id=id,
        date=date,
        owner=owner,
        new_owner=new_owner,
        car_id=car_id,

    )


class Transfer(db.Model):
    __tablename__ = 'transfers'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    owner = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    new_owner = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    car = db.relationship('Cars', backref='transfers')
    owner_user = db.relationship('User', foreign_keys=[owner])
    new_owner_user = db.relationship('User', foreign_keys=[new_owner])
    def __repr__(self):
        return f"<Transferencia {self.id} {self.date} {self.owner} {self.new_owner}>"

    def to_json(self):
        transfers = {
            'id': self.id,
            'date': self.date,
            'owner': self.owner,
            'new_owner': self.new_owner,
            'car_id': self.car_id,
        }
        return transfers