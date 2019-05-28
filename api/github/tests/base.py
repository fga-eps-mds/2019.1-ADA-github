# api/github/tests/base.py

from flask_testing import TestCase
from github import create_app
from github.data import init_db


class BaseTestCase(TestCase):
    def setUp(self):
        self.db = init_db()

    def create_app(self):
        app = create_app()
        app.config.from_object("github.config.TestingConfig")
        return app

    def tearDown(self):
        self.db.drop_database('api')
