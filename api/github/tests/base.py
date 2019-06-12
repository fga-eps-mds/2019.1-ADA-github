# api/github/tests/base.py

from flask_testing import TestCase
from github import create_app
from github.data import init_db
import os
from github.data.user import User
from github.data.project import Project


class BaseTestCase(TestCase):
    def setUp(self):
        self.db = init_db()
        self.user = User()
        self.user.username = 'sudjoao'
        self.user.chat_id = '339847919'
        self.user.github_user = 'sudjoao'
        self.user.github_user_id = '46005310'
        self.user.access_token = os.getenv("GITHUB_API_TOKEN", "")
        self.project = Project()
        self.project.name = 'apitest'
        self.project_id = '185474581'
        self.project.save()
        self.user.project = self.project
        self.user.save()
        self.GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN", "")

    def create_app(self):
        app = create_app()
        app.config.from_object("github.config.TestingConfig")
        return app

    def tearDown(self):
        self.db.drop_database('api')
