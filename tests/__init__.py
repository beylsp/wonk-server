import unittest
from wonk import create_app
from wonk.models.users import db

app = create_app('testing')


class NeuralTestCase(unittest.TestCase):
    def setUp(self):
        self.test_client = app.test_client()
        with app.app_context():
            db.create_all()
            self.populate_db()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def populate_db(self):
        pass
