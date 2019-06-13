import json
from github.tests.base import BaseTestCase
from github.tests.jsonschemas.pull_request.schemas import\
    not_found_schema, valid_pull_request_schema,\
    invalid_project_schema
from jsonschema import validate
from github.pull_request.utils import PullRequest
from requests.exceptions import HTTPError
from unittest.mock import patch
from requests import Response


class TestPullRequest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.pull_request = PullRequest(self.user.chat_id)
        mocked_content = [{
            "title": "abcdefg",
            "html_url": "https://www.google.com.br"
        }]
        mocked_content_binary = json.dumps(mocked_content).encode('utf-8')
        self.mocked_valid_response = Response()
        self.mocked_valid_response._content = mocked_content_binary
        self.mocked_valid_response.status_code = 200

    @patch('github.utils.github_utils.get')
    def test_utils_get_pull_requests(self, mocked_get):
        mocked_get.return_value = self.mocked_valid_response
        pull_requests_data = self.pull_request.get_pull_requests(
                            self.user.github_user, self.project.name)
        validate(pull_requests_data, valid_pull_request_schema)

    @patch('github.utils.github_utils.get')
    def test_utils_get_pull_requests_invalid_username(self, mocked_get):
        mocked_get.return_value = self.response_not_found
        project_owner = "wrong_user"
        with self.assertRaises(HTTPError) as context:
            self.pull_request.get_pull_requests(project_owner,
                                                self.project.name)
        notfound_json = json.loads(str(context.exception))
        self.assertEqual(notfound_json["status_code"], 404)
        validate(notfound_json, invalid_project_schema)

    @patch('github.utils.github_utils.get')
    def test_views_get_pull_request(self, mocked_get):
        mocked_get.return_value = self.mocked_valid_response
        response = self.client.get("/pullrequest/{chat_id}".format(
                                    chat_id=self.user.chat_id))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, valid_pull_request_schema)

    @patch('github.utils.github_utils.get')
    def test_views_pull_request_invalid_username(self, mocked_get):
        mocked_get.return_value = self.response_not_found
        self.user.github_user = "wrong_user"
        self.user.save()
        response = self.client.get("/pullrequest/{chat_id}".format(
                                    chat_id=self.user.chat_id))
        data = json.loads(response.data.decode())
        pull_request_string = json.dumps(not_found_schema)
        pull_request_json = json.loads(pull_request_string)
        self.assertEqual(response.status_code, 404)
        validate(data, pull_request_json)

    def test_views_pull_request_attribute_error(self):
        response = self.client.get("/pullrequest/{chat_id}".format(
                                    chat_id=None))
        data = json.loads(response.data.decode())
        pull_request_string = json.dumps(not_found_schema)
        pull_request_json = json.loads(pull_request_string)
        self.assertEqual(response.status_code, 404)
        validate(data, pull_request_json)
