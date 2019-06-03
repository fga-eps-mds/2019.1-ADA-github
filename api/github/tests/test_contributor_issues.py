import json

from github.tests.base import BaseTestCase
from github.tests.jsonschemas.contributor_issues.schemas import\
    get_contributor_issues_schema
from jsonschema import validate
import os
from github.data.user import User
from github.data.project import Project

GITHUB_API_TOKEN = os.environ.get("GITHUB_API_TOKEN", "")
CHAT_ID = os.environ.get("CHAT_ID", "")


class TestContributorIssues(BaseTestCase):
    def setup(self):
        super().setUp()
        Project.drop_collection()
        User.drop_collection()

    def test_get_contributor_issues(self):
        project = Project()
        project.name = "apitest"
        project.save()

        user = User()
        user.access_token = GITHUB_API_TOKEN
        user.chat_id = CHAT_ID
        user.github_user = "sudjoao"
        user.project = project.id
        user.save()

        response = self.client.get("/api/get_contributor_issues/{chat_id}/"
                                   "{contributor_username}"
                                   .format(
                                    chat_id=CHAT_ID,
                                    contributor_username=user.github_user))
        data = json.loads(response.data.decode())
        user_string = json.dumps(get_contributor_issues_schema)
        user_json = json.loads(user_string)
        self.assertEqual(response.status_code, 200)
        validate(data, user_json)
