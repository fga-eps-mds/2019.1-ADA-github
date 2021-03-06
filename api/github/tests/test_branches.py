import json
from github.tests.base import BaseTestCase
from github.tests.jsonschemas.branches.schemas import\
    unauthorized_schema, not_found_schema,\
    valid_branches_names_schema, invalid_project_schema
from jsonschema import validate
from github.branches.utils import Branch
from requests.exceptions import HTTPError
from unittest.mock import patch
from requests import Response


class TestBranches(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.branch = Branch(self.user.chat_id)
        self.mocked_valid_names_response = Response()
        mocked_names_content = [
            {
                "name": "master"
             }]
        content_names_binary = json.dumps(mocked_names_content).encode('utf-8')
        self.mocked_valid_names_response._content = content_names_binary
        self.mocked_valid_names_response.status_code = 200

        self.mocked_valid_date_response = Response()
        mocked_date_content = {
            "commit": {
                "commit": {
                    "author": {
                        "date": "2019-06-03T09:44:50z"
                    }
                }
            }
        }
        content_dates_binary = json.dumps(mocked_date_content).encode('utf-8')
        self.mocked_valid_date_response._content = content_dates_binary
        self.mocked_valid_date_response.status_code = 200
        self.response_not_found = Response()
        self.response_not_found.status_code = 404
        self.response_unauthorized = Response()
        self.response_unauthorized.status_code = 401

    @patch('github.utils.github_utils.get')
    def test_utils_get_branches_names(self, mocked_get):
        mocked_get.return_value = self.mocked_valid_names_response
        project_owner = self.user.github_user
        project = self.user.project
        branches_name = self.branch.get_branches_names(project_owner,
                                                       project.name)
        validate(branches_name, valid_branches_names_schema)

    @patch('github.utils.github_utils.get')
    def test_utils_get_branches_names_invalid_username(self, mocked_get):
        mocked_get.return_value = self.response_not_found
        mocked_get.raise_for_status.side_effect = HTTPError
        project_owner = "wrong_user"
        with self.assertRaises(HTTPError) as context:
            self.branch.get_branches_names(project_owner,
                                           self.project.name)
        notfound_json = json.loads(str(context.exception))
        self.assertEqual(notfound_json["status_code"], 404)
        validate(notfound_json, invalid_project_schema)

    @patch('github.utils.github_utils.get')
    def test_utils_get_branches_names_invalid_token(self, mocked_get):
        mocked_get.return_value = self.response_unauthorized
        mocked_get.raise_for_status.side_effect = HTTPError
        self.user.access_token = "wrong_token"
        self.user.save()
        wrong_branch = Branch(self.user.chat_id)
        with self.assertRaises(HTTPError) as context:
            wrong_branch.get_branches_names(self.user.github_user,
                                            self.project.name)
        unauthorized_json = json.loads(str(context.exception))
        self.assertEqual(unauthorized_json["status_code"], 401)
        validate(unauthorized_json, unauthorized_schema)

    @patch('github.utils.github_utils.get')
    def test_utils_get_date_last_commit_branches(self, mocked_get):
        mocked_get.side_effect = (self.mocked_valid_names_response,
                                  self.mocked_valid_date_response)
        branches_name = self.branch.get_date_last_commit_branches(
                        self.project.name, self.user.github_user)
        validate(branches_name, valid_branches_names_schema)

    @patch('github.utils.github_utils.get')
    def test_utils_get_date_last_commit_branches_invalid_username(self,
                                                                  mocked_get):
        mocked_get.return_value = self.response_not_found
        mocked_get.raise_for_status.side_effect = HTTPError
        project_owner = "wrong_user"
        with self.assertRaises(HTTPError) as context:
            self.branch.get_date_last_commit_branches(
                self.project.name, project_owner)
        notfound_json = json.loads(str(context.exception))
        self.assertEqual(notfound_json["status_code"], 404)
        validate(notfound_json, invalid_project_schema)

    @patch('github.utils.github_utils.get')
    def test_utils_get_date_last_commit_branches_invalid_token(self,
                                                               mocked_get):
        mocked_get.return_value = self.response_unauthorized
        self.user.access_token = "wrong_token"
        self.user.save()
        wrong_branch = Branch(self.user.chat_id)
        with self.assertRaises(HTTPError) as context:
            wrong_branch.get_date_last_commit_branches(
                self.project.name, self.user.github_user)
        unauthorized_json = json.loads(str(context.exception))
        self.assertEqual(unauthorized_json["status_code"], 401)
        validate(unauthorized_json, unauthorized_schema)

    @patch('github.utils.github_utils.get')
    def test_views_branches_names(self, mocked_get):
        mocked_get.return_value = self.mocked_valid_names_response
        response = self.client.get("/branches/names/{chat_id}".format(
                                    chat_id=self.user.chat_id))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, valid_branches_names_schema)

    @patch('github.utils.github_utils.get')
    def test_views_branches_names_invalid_username(self, mocked_get):
        mocked_get.return_value = self.response_not_found
        self.user.github_user = "wrong_user"
        self.user.save()
        response = self.client.get("/branches/names/{chat_id}".format(
                                    chat_id=self.user.chat_id))
        data = json.loads(response.data.decode())
        branches_names_string = json.dumps(not_found_schema)
        branches_names_json = json.loads(branches_names_string)
        self.assertEqual(response.status_code, 404)
        validate(data, branches_names_json)

    def test_views_branches_names_attribute_error(self):
        response = self.client.get("/branches/names/{chat_id}".format(
                                    chat_id=None))
        data = json.loads(response.data.decode())
        branches_names_string = json.dumps(not_found_schema)
        branches_names_json = json.loads(branches_names_string)
        self.assertEqual(response.status_code, 404)
        validate(data, branches_names_json)

    @patch('github.utils.github_utils.get')
    def test_views_date_commits(self, mocked_get):
        mocked_get.side_effect = (self.mocked_valid_names_response,
                                  self.mocked_valid_date_response)
        response = self.client.get("/branches/datecommits/{chat_id}".format(
                                    chat_id=self.user.chat_id))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, valid_branches_names_schema)
