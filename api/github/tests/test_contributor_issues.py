import json

from github.tests.base import BaseTestCase
from github.tests.jsonschemas.contributor_issues.schemas import\
    get_contributor_issues_schema, get_invalid_contributor_issues_schema
from jsonschema import validate
import os
from github.data.user import User
from github.data.project import Project

GITHUB_API_TOKEN = os.environ.get("GITHUB_API_TOKEN", "")


class TestContributorIssues(BaseTestCase):
    def setUp(self):
        super().setUp()
        Project.drop_collection()
        User.drop_collection()
        self.user = User()
        self.user.access_token = str(GITHUB_API_TOKEN)
        self.user.chat_id = "1234"
        self.user.github_user = "sudjoao"
        self.user.save()

    def test_get_contributor_issues(self):
        project = Project()
        project.name = "sudjoao/apitest"
        project.save()
        self.user.project = project.id
        self.user.save()
        chat_id = self.user.chat_id
        username = self.user.github_user
        response = self.client.get("/api/get_contributor_issues/{chat_id}/"
                                   "{contributor_username}"
                                   .format(
                                    chat_id=chat_id,
                                    contributor_username=username))
        data = json.loads(response.data.decode())
        user_string = json.dumps(get_contributor_issues_schema)
        user_json = json.loads(user_string)
        self.assertEqual(response.status_code, 200)
        validate(data, user_json)

    def test_invalid_get_contributor_issues(self):
        project = Project()
        project.name = "invalid_project"
        project.save()
        self.user.project = project.id
        self.user.save()
        username = self.user.github_user
        response = self.client.get("/api/get_contributor_issues/{chat_id}/"
                                   "{contributor_username}"
                                   .format(
                                    chat_id=self.user.chat_id,
                                    contributor_username=username))
        data = json.loads(response.data.decode())
        user_string = json.dumps(get_invalid_contributor_issues_schema)
        user_json = json.loads(user_string)
        self.assertEqual(response.status_code, 404)
        validate(data, user_json)

    def test_atribute_error_get_contributor_issues(self):
        project = Project()
        project.name = "invalid_project"
        project.save()
        self.user.project = project.id
        self.user.save()
        username = self.user.github_user
        response = self.client.get("/api/get_contributor_issues/{chat_id}/"
                                   "{contributor_username}"
                                   .format(
                                    chat_id="invalid",
                                    contributor_username=username))
        data = json.loads(response.data.decode())
        user_string = json.dumps(get_invalid_contributor_issues_schema)
        user_json = json.loads(user_string)
        self.assertEqual(response.status_code, 404)
        validate(data, user_json)
