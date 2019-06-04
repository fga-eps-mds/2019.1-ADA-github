import json
from github.tests.base import BaseTestCase
from github.tests.jsonschemas.branches.schemas import\
    ping_schema, unauthorized_schema, not_found_schema,\
    valid_branches_names_schema, invalid_project_schema
from jsonschema import validate
from github.branches.utils import Branch
from github.data.user import User
from github.data.project import Project
from requests.exceptions import HTTPError
import os
import sys


class TestBranches(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.branch = Branch(self.user.chat_id)

    def test_utils_get_branches_names(self):
        project_owner = self.user.github_user
        project = self.user.project
        branches_name = self.branch.get_branches_names(project_owner,
                                                       project.name)
        validate(branches_name, valid_branches_names_schema)

    def test_utils_get_branches_names_invalid_username(self):
        project_owner = "wrong_user"
        with self.assertRaises(HTTPError) as context:
            self.branch.get_branches_names(project_owner,
                                           self.project.name)
        notfound_json = json.loads(str(context.exception))
        self.assertEqual(notfound_json["status_code"], 404)
        validate(notfound_json, invalid_project_schema)

    def test_utils_get_branches_names_invalid_token(self):
        self.user.access_token = "wrong_token"
        self.user.save()
        wrong_branch = Branch(self.user.chat_id)
        with self.assertRaises(HTTPError) as context:
            wrong_branch.get_branches_names(self.user.github_user,
                                            self.project.name)
        unauthorized_json = json.loads(str(context.exception))
        self.assertEqual(unauthorized_json["status_code"], 401)
        validate(unauthorized_json, unauthorized_schema)

    def test_utils_get_date_last_commit_branches(self):
        branches_name = self.branch.get_date_last_commit_branches(
                        self.project.name, self.user.github_user)
        validate(branches_name, valid_branches_names_schema)

    def test_utils_get_date_last_commit_branches_invalid_username(self):
        project_owner = "wrong_user"
        with self.assertRaises(HTTPError) as context:
            self.branch.get_date_last_commit_branches(
                self.project.name, project_owner)
        notfound_json = json.loads(str(context.exception))
        self.assertEqual(notfound_json["status_code"], 404)
        validate(notfound_json, invalid_project_schema)

    def test_utils_get_date_last_commit_branches_invalid_token(self):
        self.user.access_token = "wrong_token"
        self.user.save()
        wrong_branch = Branch(self.user.chat_id)
        with self.assertRaises(HTTPError) as context:
            wrong_branch.get_date_last_commit_branches(
                self.project.name, self.user.github_user)
        unauthorized_json = json.loads(str(context.exception))
        self.assertEqual(unauthorized_json["status_code"], 401)
        validate(unauthorized_json, unauthorized_schema)

    def test_views_branches_names(self):
        response = self.client.get("/branches/names/{chat_id}".format(
                                    chat_id=self.user.chat_id))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, valid_branches_names_schema)

    def test_views_branches_names_invalid_username(self):
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

    def test_views_date_commits(self):
        response = self.client.get("/branches/datecommits/{chat_id}".format(
                                    chat_id=self.user.chat_id))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, valid_branches_names_schema)
