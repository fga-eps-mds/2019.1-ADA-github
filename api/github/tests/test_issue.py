import json
from github.tests.base import BaseTestCase
from github.tests.jsonschemas.issue.schemas import\
    create_issue_schema, not_found_schema, comment_issue_schema
from github.issue.utils import Issue
from jsonschema import validate
from unittest.mock import patch
from requests import Response


class TestIssue(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.issue = Issue(self.user.chat_id)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.user.access_token
            }
        self.issue_body = {
            "title": "Criando uma dsasaasd.",
            "body": " Teste utilizando JSON post"
            }
        self.comment_body = {
            "body": "Testando classe comment issue",
            "issue_number": "3"
            }
        self.mocked_valid_response = Response()
        mocked_content = {
            "title": "isso é uma nova issue",
            "body": "este é o corpo dessa issue",
            "html_url": "www.google.com.br"
        }
        content_in_binary = json.dumps(mocked_content).encode('utf-8')
        self.mocked_valid_response._content = content_in_binary
        self.mocked_valid_response.status_code = 200

    @patch('github.utils.github_utils.get')
    def test_view_create_issue(self, mocked_get):
        mocked_get.return_value = self.mocked_valid_response
        response = self.client.post("/api/new_issue/"
                                    "{chat_id}".format(
                                     chat_id=self.user.chat_id),
                                    headers=self.headers,
                                    data=json.dumps(self.issue_body))
        data = json.loads(response.data.decode())
        create_issue_string = json.dumps(create_issue_schema)
        create_issue_json = json.loads(create_issue_string)
        self.assertEqual(response.status_code, 200)
        validate(data, create_issue_json)
    def test_view_comment_issue(self):
        response = self.client.post("/api/comment_issue/"
                                    "{chat_id}".format(
                                     chat_id=self.user.chat_id),
                                    headers=self.headers,
                                    data=json.dumps(self.comment_body))
        data = json.loads(response.data.decode())
        comment_issue_string = json.dumps(comment_issue_schema)
        comment_issue_json = json.loads(comment_issue_string)
        self.assertEqual(response.status_code, 200)
        validate(data, comment_issue_json)

    def test_view_create_issue_invalid_chat_id(self):
        chat_id = "abcdefghij"
        response = self.client.post("/api/new_issue/"
                                    "{chat_id}".format(
                                     chat_id=chat_id),
                                    headers=self.headers,
                                    data=json.dumps(self.issue_body))
        data = json.loads(response.data.decode())
        create_issue_string = json.dumps(not_found_schema)
        create_issue_json = json.loads(create_issue_string)
        self.assertEqual(response.status_code, 404)
        validate(data, create_issue_json)

    def test_view_create_issue_invalid_token(self):
        self.user.access_token = "wrong_token"
        self.user.save()
        response = self.client.post("/api/new_issue/"
                                    "{chat_id}".format(
                                     chat_id=self.user.chat_id),
                                    headers=self.headers,
                                    data=json.dumps(self.issue_body))
        data = json.loads(response.data.decode())
        create_issue_string = json.dumps(not_found_schema)
        create_issue_json = json.loads(create_issue_string)
        self.assertEqual(response.status_code, 401)
        validate(data, create_issue_json)


    def test_view_comment_issue_invalid_chat_id(self):
        chat_id = "qweqweqrasd"
        response = self.client.post("/api/comment_issue/"
                                    "{chat_id}".format(
                                        chat_id=chat_id),
                                    headers=self.headers,
                                    data=json.dumps(self.comment_body))
        data = json.loads(response.data.decode())
        comment_issue_string = json.dumps(not_found_schema)
        comment_issue_json = json.loads(comment_issue_string)
        self.assertEqual(response.status_code, 404)
        validate(data, comment_issue_json)

    def test_view_comment_issue_invalid_token(self):
        self.user.access_token = "wrong_token"
        self.user.save()
        response = self.client.post("/api/comment_issue/"
                                    "{chat_id}".format(
                                        chat_id=self.user.chat_id),
                                    headers=self.headers,
                                    data=json.dumps(self.comment_body))
        data = json.loads(response.data.decode())
        comment_issue_string = json.dumps(not_found_schema)
        comment_issue_json = json.loads(comment_issue_string)
        self.assertEqual(response.status_code, 401)
        validate(data, comment_issue_json)
