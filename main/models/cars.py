from sqlalchemy import String, Column, Integer

from main import db
from sqlalchemy.ext.hybrid import hybrid_property


class Cars(db.Model):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True)
    brand = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    year = Column(String(50), nullable=False)
    user_id = Column(Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Car {self.brand} {self.model} {self.year} {self.user_id}>'

