import unittest

from sqlalchemy import text
from sqlalchemy.future import engine

from main import create_app, db


class ConnectionTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # test connection to db
    def test_db_connection(self):
        sql = f"SELECT 'Hello world'"
        with db.engine.connect() as conn:
            result = conn.execute(text(sql))
        self.assertEqual(result.fetchone()[0], 'Hello world')