from requests import Response
from github.find_project_collaborators.utils import FindProjectCollaborators
from github.tests.base import BaseTestCase
from github.tests.jsonschemas.find_project_collaborators.schemas import \
     collaborators_valid_schema, invalid_project_schema
import os
import json
from jsonschema import validate
from unittest.mock import patch


class TestFindProjectCollaborators(BaseTestCase):
    access_token = os.getenv("GITHUB_API_TOKEN", "")

    def setUp(self):
        super().setUp()
        self.find_project_collaborators = FindProjectCollaborators(
            self.user.chat_id)
        self.mocked_get_project = Response()
        self.mocked_get_project.status_code = 200
        get_project_response_content = [
            {
                "name": "apitest",
                "full_name": "sudjoao/apitest"
            }]
        get_project_content_in_binary = json.\
            dumps(get_project_response_content).encode('utf-8')
        self.mocked_get_project._content = \
            get_project_content_in_binary

        self.mocked_get_collaborators = Response()
        self.mocked_get_collaborators.status_code = 200
        get_collaborators_reponse_content = [
            {
                "login": "sudjoao"
            }]
        get_collaborators_content_in_binary = json.\
            dumps(get_collaborators_reponse_content).encode('utf-8')
        self.mocked_get_collaborators._content = \
            get_collaborators_content_in_binary

    @patch('github.utils.github_utils.get')
    def test_utils_get_project(self, mocked_get):
        mocked_get.return_value = self.mocked_get_project
        project_name = self.project.name
        project_collaborators = self.find_project_collaborators\
            .get_project(project_name)
        full_name = "sudjoao/apitest"
        self.assertEqual(project_collaborators, full_name)

    @patch('github.utils.github_utils.get')
    def test_views_find_collaborators(self, mocked_get):
        mocked_get.side_effect = (self.mocked_get_project,
                                  self.mocked_get_collaborators)

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

    @patch('github.utils.github_utils.get')
    def test_views_find_collaborators_invalid_token(self, mocked_get):
        mocked_get.return_value = self.response_unauthorized
        self.user.access_token = "wrong_token"
        self.user.save()
        response = self.client.get("/api/find_collaborators/{chat_id}".format(
            chat_id=self.user.chat_id))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        validate(data, invalid_project_schema)
