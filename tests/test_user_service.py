import unittest
from main import create_app, db
from main.models import User
from main.services.user_service import UserService


class TestUserService(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.userService = UserService()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user(self):
        user_model = User(name='Delfina', last_name='quinteros', email='delfina@gmail.com', dni='12345678', address='calle falsa 123', password='123456789', algorand_address='nsdnfskldgfnlasdnjfñdnfdffsdfsdfnedkfn', id=1, cars=None)
        self.userService.create(user_model)
        self.assertGreater(user_model.id, 0)
        user1 = self.userService.find_by_id(1)
        self.assertIsNotNone(user1)

    def test_create_user(self):
        user = self.__create_user()
        self.assertEqual(user.name, 'delfina')
        self.assertEqual(user.last_name, 'quinteros')
        self.assertEqual(user.dni, '12345678')
        self.assertEqual(user.address, 'calle falsa 123')
        self.assertEqual(user.password, '123456789')
        self.assertEqual(user.cars, 'Toyota Corolla 2015')
        self.assertEqual(user.algorand_address, 'nsdnfskldgfnlasdnjfñdnfdffsdfsdfnedkfn')
        self.assertGreater(user.id, 0)
        self.assertEqual(user.email, 'delfina@gmail.com')

    def test_db_find_by_user(self):
        user = self.__create_user()
        user = self.userService.find_by_username(user.name)
        self.assertEqual(user.name, 'delfina')
        self.assertGreater(user.id, 0)

    def __create_user(self):
        name = 'delfina'
        last_name = 'quinteros'
        email = 'delfina@gmail.com'
        dni = '12345678'
        address = 'calle falsa 123'
        password = '123456789'
        id= 1
        algorand_address = 'nsdnfskldgfnlasdnjfñdnfdffsdfsdfnedkfn'
        cars = 'Toyota Corolla 2015'
        user = User(name=name, last_name=last_name, email=email, dni=dni, address=address, password=password, algorand_address=algorand_address, id=id, cars=cars)
        return self.userService.create(user)
