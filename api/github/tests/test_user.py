import json
import unittest
from github.data.user import User
from github.tests.base import BaseTestCase
from github.tests.jsonschemas.user.schemas import\
    ping_schema, view_get_access_token_schema,\
    view_get_repos_schema, view_get_github_login_schema,\
    invalid_view_get_repos_schema, view_notfound_get_github_login_schema,\
    view_register_repository_schema, view_notfound_register_repository_schema
from jsonschema import validate
import os

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "")
GITHUB_API_TOKEN = os.environ.get("GITHUB_API_TOKEN", "")


class TestUser(BaseTestCase):
    def setUp(self):
        super().setUp()
        User.drop_collection()
        self.user = User()
        self.user.access_token = str(GITHUB_API_TOKEN)
        self.user.github_user = "caiovfernandes"
        self.user.chat_id = "662358971"
        self.user.save()

    def test_ping_pong(self):
        response = self.client.get("/user/ping")
        data = json.loads(response.data.decode())
        ping_string = json.dumps(ping_schema)
        ping_json = json.loads(ping_string)
        self.assertEqual(response.status_code, 200)
        validate(data, ping_json)

    def test_view_get_access_token(self):
        chat_id = self.user.chat_id
        response = self.client.get("/user/github/authorize/{chat_id}"
                                   .format(chat_id=chat_id))
        self.assertEquals(response.status_code, 302)

    def invalid_test_view_get_access_token(self):
        chat_id = "12"
        response = self.client.get("/user/github/authorize/{chat_id}"
                                   .format(chat_id=chat_id))
        data = response.data.decode()
        user_string = json.dumps(view_get_access_token_schema)
        user_json = json.loads(user_string)
        self.assertEquals(response.status_code, 302)
        validate(data, user_json)

    def test_view_get_repos(self):
        username = self.user.github_user
        response = self.client.get("/user/{github_username}/repositories"
                                   .format(github_username=username))
        data = json.loads(response.data.decode())
        user_string = json.dumps(view_get_repos_schema)
        user_json = json.loads(user_string)
        self.assertEqual(response.status_code, 200)
        validate(data, user_json)

    def test_notfound_view_get_repos(self):
        username = "false"
        response = self.client.get("/user/{github_username}/repositories"
                                   .format(github_username=username))
        data = json.loads(response.data.decode())
        user_string = json.dumps(invalid_view_get_repos_schema)
        user_json = json.loads(user_string)
        self.assertEqual(response.status_code, 404)
        validate(data, user_json)

    def test_view_get_github_login(self):
        chat_id = self.user.chat_id
        response = self.client.get("/user/{chat_id}"
                                   .format(chat_id=chat_id))

        data = json.loads(response.data.decode())
        user_string = json.dumps(view_get_github_login_schema)
        user_json = json.loads(user_string)
        self.assertEqual(response.status_code, 200)
        validate(data, user_json)

    def test_notfound_view_get_github_login(self):
        chat_id = 123
        response = self.client.get("/user/{chat_id}"
                                   .format(chat_id=chat_id))

        data = json.loads(response.data.decode())
        user_string = json.dumps(view_notfound_get_github_login_schema)
        user_json = json.loads(user_string)
        self.assertEqual(response.status_code, 404)
        validate(data, user_json)

    def test_view_register_repository(self):
        header = {
             "Content-Type": "application/json"
        }
        data = {
            "repository_name": "eda",
            "chat_id": self.user.chat_id
        }
        data_json = json.dumps(data)
        response = self.client.post("/user/repo",
                                    headers=header, data=data_json)
        data = json.loads(response.data.decode())
        user_string = json.dumps(view_register_repository_schema)
        user_json = json.loads(user_string)
        self.assertEqual(response.status_code, 200)
        validate(data, user_json)

    def test_notfound_view_register_repository(self):
        header = {
             "Content-Type": "application/json"
        }
        data = {
            "repository_name": "eda",
            "chat_id": "1234"
        }
        data_json = json.dumps(data)
        response = self.client.post("/user/repo",
                                    headers=header, data=data_json)
        data = json.loads(response.data.decode())
        user_string = json.dumps(view_notfound_register_repository_schema)
        user_json = json.loads(user_string)
        self.assertEqual(response.status_code, 400)
        validate(data, user_json)

        if __name__ == "__main__":
            unittest.main()
