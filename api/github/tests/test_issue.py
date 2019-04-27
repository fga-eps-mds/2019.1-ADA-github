import json
import unittest
from github.tests.base import BaseTestCase
from github.tests.jsonschemas.issue.schemas import\
    ping_schema
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

if __name__ == "__main__":
    unittest.main()
