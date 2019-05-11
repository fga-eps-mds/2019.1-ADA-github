import json
import unittest
from github.tests.base import BaseTestCase
from github.tests.jsonschemas.schemas import\
    ping_schema, create_issue_schema
from jsonschema import validate
import os


class TestBuild(BaseTestCase):
    def test_ping_pong(self):
        response = self.client.get("/issue/ping")
        data = json.loads(response.data.decode())
        ping_string = json.dumps(ping_schema)
        ping_json = json.loads(ping_string)
        self.assertEqual(response.status_code, 200)
        validate(data, ping_json)

    def test_view_create_issue(self):
        repository_name = "PPC"
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
                             "{repository_name}".format(
                             repository_name = repository_name), headers=headers, data=json.dumps(issue_body))

        data = json.loads(response.data.decode())
        create_issue_string = json.dumps(create_issue_schema)
        create_issue_json = json.loads(create_issue_string)
        self.assertEqual(response.status_code, 200)
        validate(data, create_issue_json)


if __name__ == "__main__":
    unittest.main()
