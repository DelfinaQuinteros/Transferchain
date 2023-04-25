from main.repositories import CarsRepository
from main.models import Cars


class CarsService:

    def __init__(self):
        self.repository = CarsRepository()

    def create(self, car: Cars) -> Cars:
        car = self.repository.create(car)
        return car

    def find_by_id(self, id):
        car = self.repository.find_by_id(id)
        return car

    def find_all(self):
        cars = self.repository.find_all()
        return cars

    def update(self, car: Cars) -> Cars:
        car = self.repository.update(car)
        return car

