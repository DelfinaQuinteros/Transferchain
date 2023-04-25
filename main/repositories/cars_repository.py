from .. import db
from main.repositories import Create, Read, Update
from main.models import Cars


class CarsRepository(Create, Read, Update):

    def __init__(self):
        self.__car = Cars

    def create(self, model: db.Model) -> Cars:
        db.session.add(model)
        db.session.commit()
        return model

    def find_all(self):
        return db.session.query(self.__car).all()

    def find_by_id(self, id: int) -> Cars:
        return db.session.query(self.__car).get(id)

    def update(self, car: Cars) -> Cars:
        db.session.add(car)
        db.session.commit()
        return car
