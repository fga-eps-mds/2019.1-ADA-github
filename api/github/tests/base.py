# api/github/tests/base.py

from flask_testing import TestCase
from github import create_app


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app()
        app.config.from_object("github.config.TestingConfig")
        return app
