import json
import unittest
from github.tests.base import BaseTestCase
from github.tests.jsonschemas.schemas import\
    ping_schema, create_issue_schema,\
    not_found_schema, not_found_user_schema
from github.issue.utils import Issue
from jsonschema import validate
import os
from requests.exceptions import HTTPError


class TestIssue(BaseTestCase):
    def test_ping_pong(self):
        response = self.client.get("/issue/ping")
        data = json.loads(response.data.decode())
        ping_string = json.dumps(ping_schema)
        ping_json = json.loads(ping_string)
        self.assertEqual(response.status_code, 200)
        validate(data, ping_json)

    # def test_view_create_issue(self):
    #     chat_id = "662358971"
    #     issue_body = {
    #         "title": "Criando uma dsasaasd.",
    #         "body": " Teste utilizando JSON post"
    #         }

    #     GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN", "")
    #     headers = {
    #         "Content-Type": "application/json",
    #         "Authorization": "Bearer " + GITHUB_API_TOKEN
    #         }

    #     response = self.client.post("/api/new_issue/"
    #                                 "{chat_id}".format(
    #                                  chat_id=chat_id),
    #                                 headers=headers,
    #                                 data=json.dumps(issue_body))

    #     data = json.loads(response.data.decode())
    #     create_issue_string = json.dumps(create_issue_schema)
    #     create_issue_json = json.loads(create_issue_string)
    #     self.assertEqual(response.status_code, 200)
    #     validate(data, create_issue_json)

    def test_view_create_issue_invalid_chat_id(self):
        chat_id = "abcdefghij"
        issue_body = {
            "title": "Criando uma dsasaasd.",
            "body": " Teste utilizando JSON post"
            }

        GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN", "")
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + GITHUB_API_TOKEN
            }

        response = self.client.post("/api/new_issue/"
                                    "{chat_id}".format(
                                     chat_id=chat_id),
                                    headers=headers,
                                    data=json.dumps(issue_body))

        data = json.loads(response.data.decode())
        create_issue_string = json.dumps(not_found_schema)
        create_issue_json = json.loads(create_issue_string)
        self.assertEqual(response.status_code, 404)
        validate(data, create_issue_json)

    def test_view_create_issue_invalid_token(self):
        chat_id = "abcdefghij"
        issue_body = {
            "title": "Criando uma dsasaasd.",
            "body": " Teste utilizando JSON post"
            }

        GITHUB_API_TOKEN = "123456789"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + GITHUB_API_TOKEN
            }

        response = self.client.post("/api/new_issue/"
                                    "{chat_id}".format(
                                     chat_id=chat_id),
                                    headers=headers,
                                    data=json.dumps(issue_body))
        data = json.loads(response.data.decode())
        create_issue_string = json.dumps(not_found_schema)
        create_issue_json = json.loads(create_issue_string)
        self.assertEqual(response.status_code, 404)
        validate(data, create_issue_json)

    def test_utils_create_issue(self):
        GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN", "")
        issue = Issue(GITHUB_API_TOKEN)
        repository_name = "apitest"
        username = "sudjoao"
        title = "Test Create Issue"
        body = " Teste utilizando JSON post"

        created_issue = issue.create_issue(repository_name, username,
                                           title, body)
        validate(created_issue, create_issue_schema)

    def test_incorrect_username_utils_create_issue(self):
        GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN", "")
        issue = Issue(GITHUB_API_TOKEN)
        repository_name = "apitest"
        username = "lalala"
        title = "Test Create Issue"
        body = " Teste utilizando JSON post"
        with self.assertRaises(HTTPError) as context:
            issue.create_issue(repository_name, username,
                               title, body)
        unauthorized_json = json.loads(str(context.exception))
        validate(unauthorized_json, not_found_user_schema)


if __name__ == "__main__":
    unittest.main()
