import json
from github.tests.base import BaseTestCase
from github.tests.jsonschemas.pull_request.schemas import\
    ping_schema, not_found_schema, valid_pull_request_schema,\
    invalid_project_schema
from jsonschema import validate
from github.pull_request.utils import PullRequest
from github.data.user import User
from github.data import init_db
from github.data.project import Project
from requests.exceptions import HTTPError
import os


class TestPullRequest(BaseTestCase):
    def setup(self):
        init_db()
        Project.drop_collection()
        User.drop_collection()

    def test_ping_pong(self):
        response = self.client.get("/pullrequest/ping")
        data = json.loads(response.data.decode())
        ping_string = json.dumps(ping_schema)
        ping_json = json.loads(ping_string)
        self.assertEqual(response.status_code, 200)
        validate(data, ping_json)

    def test_utils_get_pull_requests(self):
        GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN", "")
        project_name = "apitest"
        project_owner = "sudjoao"
        pull_request = PullRequest(GITHUB_API_TOKEN)
        pull_requests_data = pull_request.get_pull_requests(project_owner,
                                                            project_name)
        validate(pull_requests_data, valid_pull_request_schema)

    def test_utils_get_pull_requests_invalid_username(self):
        GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN", "")
        project_name = "apitest"
        project_owner = "wrong_user"
        pull_request = PullRequest(GITHUB_API_TOKEN)
        with self.assertRaises(HTTPError) as context:
            pull_request.get_pull_requests(project_owner, project_name)
        notfound_json = json.loads(str(context.exception))
        self.assertEqual(notfound_json["status_code"], 404)
        validate(notfound_json, invalid_project_schema)

    def test_views_get_pull_request(self):
        GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN", "")
        project = Project()
        project.name = "apitest"
        project.save()
        user = User()
        user.chat_id = "00000"
        user.access_token = GITHUB_API_TOKEN
        user.github_user = "sudjoao"
        user.project = project
        user.save()
        response = self.client.get("/pullrequest/{chat_id}".format(
                                    chat_id=user.chat_id))
        data = json.loads(response.data.decode())
        User.delete(user)
        Project.delete(project)
        self.assertEqual(response.status_code, 200)
        validate(data, valid_pull_request_schema)

    def test_views_pull_request_invalid_username(self):
        GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN", "")
        project = Project()
        project.name = "apitest"
        project.save()
        user = User()
        user.chat_id = "00000"
        user.access_token = GITHUB_API_TOKEN
        user.github_user = "wrong_username"
        user.project = project
        user.save()

        response = self.client.get("/pullrequest/{chat_id}".format(
                                    chat_id=user.chat_id))
        User.delete(user)
        Project.delete(project)

        data = json.loads(response.data.decode())
        pull_request_string = json.dumps(not_found_schema)
        pull_request_json = json.loads(pull_request_string)

        self.assertEqual(response.status_code, 404)
        validate(data, pull_request_json)

    def test_views_pull_request_invalid_token(self):
        GITHUB_API_TOKEN = "abcdef"
        project = Project()
        project.name = "apitest"
        project.save()
        user = User()
        user.chat_id = "00000"
        user.access_token = GITHUB_API_TOKEN
        user.github_user = "sudjoao"
        user.project = project
        user.save()
        response = self.client.get("/pullrequest/{chat_id}".format(
                                    chat_id=user.chat_id))
        User.delete(user)
        Project.delete(project)

        data = json.loads(response.data.decode())
        pull_request_string = json.dumps(not_found_schema)
        pull_request_json = json.loads(pull_request_string)

        self.assertEqual(response.status_code, 401)
        validate(data, pull_request_json)

    def test_views_pull_request_attribute_error(self):
        GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN", "")
        project = Project()
        project.name = "apitest"
        project.save()
        user = User()
        user.chat_id = "00000"
        user.access_token = GITHUB_API_TOKEN
        user.github_user = "sudjoao"
        user.project = project
        user.save()
        response = self.client.get("/pullrequest/{chat_id}".format(
                                    chat_id=None))
        User.delete(user)
        Project.delete(project)

        data = json.loads(response.data.decode())
        pull_request_string = json.dumps(not_found_schema)
        pull_request_json = json.loads(pull_request_string)

        self.assertEqual(response.status_code, 404)
        validate(data, pull_request_json)
