import json
import unittest
from unittest.mock import patch, Mock
from github.tests.base import BaseTestCase
from github.tests.jsonschemas.user.schemas import\
    view_get_access_token_schema,\
    view_get_repos_schema, invalid_view_get_repos_schema, \
    view_register_repository_schema,\
    view_notfound_register_repository_schema, get_user_infos_schema
from jsonschema import validate
from github.user.utils import UserInfo
import os
from requests import Response
from github.user.utils import authenticate_access_token

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "")
GITHUB_API_TOKEN = os.environ.get("GITHUB_API_TOKEN", "")


class TestUser(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user_info = UserInfo(self.user.chat_id)
        self.headers = {
            "Content-Type": "application/json"
        }
        get_repo_content = [
            {
                "name": "mocked_user",
                "full_name": "mocked_user/mocked_repo"
            }
        ]
        get_repo_content_in_binary = json.dumps(get_repo_content).\
            encode('utf-8')
        self.mocked_valid_get_repo = Response()
        self.mocked_valid_get_repo._content = get_repo_content_in_binary
        self.mocked_valid_get_repo.status_code = 200
        get_own_data_content = {
            "login": "mocked_user",
            "id": "123456789"
        }
        get_own_data_content_in_binary = json.dumps(
            get_own_data_content).encode('utf-8')
        self.mocked_valid_own_data = Response()
        self.mocked_valid_own_data._content = get_own_data_content_in_binary
        self.mocked_valid_own_data.status_code = 200
        mocked_post_content = {
            "access_token": "xyz789abc123"
        }
        mocked_post_content_in_binary = json.dumps(mocked_post_content).\
            encode('utf-8')
        self.mocked_post_valid = Response()
        self.mocked_post_valid._content = mocked_post_content_in_binary
        self.mocked_post_valid.status_code = 200

    @patch('github.user.utils.telegram')
    def test_view_get_access_token(self, mocked_message):
        mocked_message.return_value = Mock()
        mocked_message.Bot.send_message = Mock()
        chat_id = self.user.chat_id
        response = self.client.get("/user/github/authorize/{chat_id}"
                                   .format(chat_id=chat_id))
        self.assertEqual(response.status_code, 302)

    @patch('github.utils.github_utils.get')
    @patch('github.user.utils.telegram')
    @patch('github.user.utils.post')
    def test_view_get_access_token_new_user(self, mocked_post,
                                            mocked_message,
                                            mocked_get):
        mocked_get.side_effect = (self.mocked_valid_own_data,
                                  self.mocked_valid_own_data,
                                  self.mocked_valid_get_repo)
        mocked_post.return_value = self.mocked_post_valid
        mocked_message.return_value = Mock()
        mocked_message.Bot.send_message = Mock()
        chat_id = "1234567890"
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

    @patch('github.utils.github_utils.get')
    def test_view_get_repos(self, mocked_get):
        mocked_get.side_effect = (self.mocked_valid_own_data,
                                  self.mocked_valid_get_repo)
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

    @patch('github.webhook.webhook_utils.delete')
    @patch('github.utils.github_utils.get')
    def test_view_register_repository(self, mocked_get, mocked_delete):
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

    @patch('github.user.utils.telegram')
    @patch('github.utils.github_utils.get')
    def test_view_change_repository(self, mocked_get, mocked_message):
        mocked_get.side_effect = (self.mocked_valid_own_data,
                                  self.mocked_valid_own_data,
                                  self.mocked_valid_get_repo)
        mocked_message.return_value = Mock()
        mocked_message.Bot.send_message = Mock()
        response = self.client.get("/user/change_repo/{chat_id}"
                                   .format(chat_id=self.user.chat_id))
        self.assertEqual(response.status_code, 200)

    @patch('github.user.utils.telegram')
    @patch('github.utils.github_utils.get')
    def test_view_change_repository_invalid(self, mocked_get, mocked_message):
        mocked_get.return_value = self.response_unauthorized
        mocked_message.return_value = Mock()
        mocked_message.Bot.send_message = Mock()
        response = self.client.get("/user/change_repo/{chat_id}"
                                   .format(chat_id=self.user.chat_id))
        self.assertEqual(response.status_code, 401)

    @patch('github.user.utils.post')
    def test_authenticate_access_token(self, mocked_post):
        mocked_response = Response()
        mocked_content = {"access_token": "6321861256"}
        content_in_binary = json.dumps(mocked_content).encode('utf-8')
        mocked_response._content = content_in_binary
        mocked_response.status_code = 200
        mocked_post.return_value = mocked_response
        authenticate_access_token("44456")

    def test_views_get_user_infos(self):
        chat_id = self.user.chat_id
        response = self.client.get("/user/infos/{chat_id}"
                                   .format(chat_id=chat_id))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, get_user_infos_schema)


if __name__ == "__main__":
    unittest.main()
