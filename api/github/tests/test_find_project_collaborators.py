from github.tests.base import BaseTestCase
from github.tests.jsonschemas.find_project_collaborators.schemas import \
     collaborators_valid_schema, invalid_project_schema
import os
import json
from jsonschema import validate


class TestFindProjectCollaborators(BaseTestCase):
    access_token = os.getenv("GITHUB_API_TOKEN", "")

    def setUp(self):
        super().setUp()

    def test_views_find_collaborators(self):
        response = self.client.get("/api/find_collaborators/{chat_id}".format(
                                    chat_id=self.user.chat_id))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, collaborators_valid_schema)

    def test_views_find_collaborators_invalid_chat_id(self):
        response = self.client.get("/api/find_collaborators/{chat_id}".format(
                                                     chat_id=None))
        data = json.loads(response.data.decode())
        self.assertEqual(data["status_code"], 404)
        validate(data, invalid_project_schema)

    def test_views_find_collaborators_invalid_token(self):
        self.user.access_token = "wrong_token"
        self.user.save()
        response = self.client.get("/api/find_collaborators/{chat_id}".format(
                                  chat_id=self.user.chat_id))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        validate(data, invalid_project_schema)
