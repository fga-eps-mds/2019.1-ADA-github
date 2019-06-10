import json
import unittest
from github.tests.base import BaseTestCase
from github.tests.jsonschemas.user.schemas import\
    view_get_access_token_schema,\
    view_get_repos_schema, invalid_view_get_repos_schema, \
    view_register_repository_schema, view_notfound_register_repository_schema
from jsonschema import validate
from github.user.utils import UserInfo
import os
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "")
GITHUB_API_TOKEN = os.environ.get("GITHUB_API_TOKEN", "")


class TestUser(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user_info = UserInfo(self.user.chat_id)
        self.headers = {
             "Content-Type": "application/json"
        }

    def test_view_get_access_token(self):
        chat_id = self.user.chat_id
        response = self.client.get("/user/github/authorize/{chat_id}"
                                   .format(chat_id=chat_id))
        self.assertEqual(response.status_code, 302)

    def invalid_test_view_get_access_token(self):
        chat_id = "12"
        response = self.client.get("/user/github/authorize/{chat_id}"
                                   .format(chat_id=chat_id))
        data = response.data.decode()
        user_string = json.dumps(view_get_access_token_schema)
        user_json = json.loads(user_string)
        self.assertEqual(response.status_code, 302)
        validate(data, user_json)

    def test_view_get_repos(self):
        response = self.client.get("/user/repositories/{chat_id}"
                                   .format(chat_id=self.user.chat_id))
        data = json.loads(response.data.decode())
        user_string = json.dumps(view_get_repos_schema)
        user_json = json.loads(user_string)
        self.assertEqual(response.status_code, 200)
        validate(data, user_json)

    def test_not_found_chat_id_view_get_repos(self):
        chat_id = "wrong_id"
        response = self.client.get("/user/repositories/{chat_id}"
                                   .format(chat_id=chat_id))
        data = json.loads(response.data.decode())
        user_string = json.dumps(invalid_view_get_repos_schema)
        user_json = json.loads(user_string)
        self.assertEqual(response.status_code, 404)
        validate(data, user_json)

    def test_view_register_repository(self):
        data = {
            "repository_name": "eda",
            "chat_id": self.user.chat_id
        }
        data_json = json.dumps(data)
        response = self.client.post("/user/repo/{chat_id}"
                                    .format(chat_id=self.user.chat_id),
                                    headers=self.headers, data=data_json)
        data = json.loads(response.data.decode())
        user_string = json.dumps(view_register_repository_schema)
        user_json = json.loads(user_string)
        self.assertEqual(response.status_code, 200)
        validate(data, user_json)

    def test_notfound_view_register_repository(self):
        data = {
            "repository_name": "eda",
            "chat_id": "1234"
        }
        data_json = json.dumps(data)
        response = self.client.post("/user/repo/{chat_id}"
                                    .format(chat_id=self.user.chat_id),
                                    headers=self.headers, data=data_json)
        data = json.loads(response.data.decode())
        user_string = json.dumps(view_notfound_register_repository_schema)
        user_json = json.loads(user_string)
        self.assertEqual(response.status_code, 404)
        validate(data, user_json)


if __name__ == "__main__":
    unittest.main()
