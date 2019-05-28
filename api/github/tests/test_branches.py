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


class TestBranches(BaseTestCase):
    def setup(self):
        super().setUp()
        Project.drop_collection()
        User.drop_collection()

    def test_ping_pong(self):
        response = self.client.get("/branches/ping")
        data = json.loads(response.data.decode())
        ping_string = json.dumps(ping_schema)
        ping_json = json.loads(ping_string)
        self.assertEqual(response.status_code, 200)
        validate(data, ping_json)

    def test_utils_get_branches_names(self):
        GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN", "")
        project_name = "apitest"
        project_owner = "sudjoao"
        branch = Branch(GITHUB_API_TOKEN)
        branches_name = branch.get_branches_names(project_name, project_owner)
        validate(branches_name, valid_branches_names_schema)

    def test_utils_get_branches_names_invalid_username(self):
        GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN", "")
        project_name = "apitest"
        project_owner = "wrong_user"
        branch = Branch(GITHUB_API_TOKEN)
        with self.assertRaises(HTTPError) as context:
            branch.get_branches_names(project_name, project_owner)
        notfound_json = json.loads(str(context.exception))
        self.assertEqual(notfound_json["status_code"], 404)
        validate(notfound_json, invalid_project_schema)

    def test_utils_get_branches_names_invalid_token(self):
        GITHUB_API_TOKEN = ("abcdefgh")
        project_name = "apitest"
        project_owner = "sudjoao"
        branch = Branch(GITHUB_API_TOKEN)
        with self.assertRaises(HTTPError) as context:
            branch.get_branches_names(project_name, project_owner)
        unauthorized_json = json.loads(str(context.exception))
        self.assertEqual(unauthorized_json["status_code"], 401)
        validate(unauthorized_json, unauthorized_schema)

    def test_utils_get_date_last_commit_branches(self):
        GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN", "")
        project_name = "apitest"
        project_owner = "sudjoao"
        branch = Branch(GITHUB_API_TOKEN)
        branches_name = branch.get_date_last_commit_branches(project_name,
                                                             project_owner)
        validate(branches_name, valid_branches_names_schema)

    def test_utils_get_date_last_commit_branches_invalid_username(self):
        GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN", "")
        project_name = "apitest"
        project_owner = "wrong_user"
        branch = Branch(GITHUB_API_TOKEN)
        with self.assertRaises(HTTPError) as context:
            branch.get_date_last_commit_branches(project_name, project_owner)
        notfound_json = json.loads(str(context.exception))
        self.assertEqual(notfound_json["status_code"], 404)
        validate(notfound_json, invalid_project_schema)

    def test_utils_get_date_last_commit_branches_invalid_token(self):
        GITHUB_API_TOKEN = ("abcdefgh")
        project_name = "apitest"
        project_owner = "sudjoao"
        branch = Branch(GITHUB_API_TOKEN)
        with self.assertRaises(HTTPError) as context:
            branch.get_date_last_commit_branches(project_name, project_owner)
        unauthorized_json = json.loads(str(context.exception))
        self.assertEqual(unauthorized_json["status_code"], 401)
        validate(unauthorized_json, unauthorized_schema)

    def test_views_branches_names(self):
        GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN", "")
        project = Project()
        project.name = "apitest"
        project.save()
        user = User()
        user.chat_id = "00000"
        user.access_token = GITHUB_API_TOKEN
        user.github_user = "sudjoao"
        user.project = project
        user.save()
        response = self.client.get("/branches/names/{chat_id}".format(
                                    chat_id=user.chat_id))
        data = json.loads(response.data.decode())
        User.delete(user)
        Project.delete(project)
        self.assertEqual(response.status_code, 200)
        validate(data, valid_branches_names_schema)

    def test_views_branches_names_invalid_username(self):
        GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN", "")
        project = Project()
        project.name = "apitest"
        project.save()
        user = User()
        user.chat_id = "00000"
        user.access_token = GITHUB_API_TOKEN
        user.github_user = "wrong_username"
        user.project = project
        user.save()

        response = self.client.get("/branches/names/{chat_id}".format(
                                    chat_id=user.chat_id))
        User.delete(user)
        Project.delete(project)

        data = json.loads(response.data.decode())
        branches_names_string = json.dumps(not_found_schema)
        branches_names_json = json.loads(branches_names_string)

        self.assertEqual(response.status_code, 404)
        validate(data, branches_names_json)

    def test_views_branches_names_invalid_token(self):
        GITHUB_API_TOKEN = "abcdef"
        project = Project()
        project.name = "apitest"
        project.save()
        user = User()
        user.chat_id = "00000"
        user.access_token = GITHUB_API_TOKEN
        user.github_user = "sudjoao"
        user.project = project
        user.save()
        response = self.client.get("/branches/names/{chat_id}".format(
                                    chat_id=user.chat_id))
        User.delete(user)
        Project.delete(project)

        data = json.loads(response.data.decode())
        branches_names_string = json.dumps(not_found_schema)
        branches_names_json = json.loads(branches_names_string)

        self.assertEqual(response.status_code, 401)
        validate(data, branches_names_json)

    def test_views_branches_names_attribute_error(self):
        GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN", "")
        project = Project()
        project.name = "apitest"
        project.save()
        user = User()
        user.chat_id = "00000"
        user.access_token = GITHUB_API_TOKEN
        user.github_user = "sudjoao"
        user.project = project
        user.save()
        response = self.client.get("/branches/names/{chat_id}".format(
                                    chat_id=None))
        User.delete(user)
        Project.delete(project)

        data = json.loads(response.data.decode())
        branches_names_string = json.dumps(not_found_schema)
        branches_names_json = json.loads(branches_names_string)

        self.assertEqual(response.status_code, 404)
        validate(data, branches_names_json)

    def test_views_date_commits(self):
        GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN", "")
        project = Project()
        project.name = "apitest"
        project.save()
        user = User()
        user.chat_id = "00000"
        user.access_token = GITHUB_API_TOKEN
        user.github_user = "sudjoao"
        user.project = project
        user.save()
        response = self.client.get("/branches/datecommits/{chat_id}".format(
                                    chat_id=user.chat_id))
        data = json.loads(response.data.decode())
        User.delete(user)
        Project.delete(project)
        self.assertEqual(response.status_code, 200)
        validate(data, valid_branches_names_schema)

    def test_views_date_commits_invalid_username(self):
        GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN", "")
        project = Project()
        project.name = "apitest"
        project.save()
        user = User()
        user.chat_id = "00000"
        user.access_token = GITHUB_API_TOKEN
        user.github_user = "wrong_user"
        user.project = project
        user.save()
        response = self.client.get("/branches/datecommits/{chat_id}".format(
                                    chat_id=user.chat_id))
        User.delete(user)
        Project.delete(project)
        data = json.loads(response.data.decode())
        date_commits_string = json.dumps(not_found_schema)
        date_commits_json = json.loads(date_commits_string)

        self.assertEqual(response.status_code, 404)
        validate(data, date_commits_json)

    def test_views_date_commits_invalid_token(self):
        GITHUB_API_TOKEN = "abcefgh"
        project = Project()
        project.name = "apitest"
        project.save()
        user = User()
        user.chat_id = "00000"
        user.access_token = GITHUB_API_TOKEN
        user.github_user = "sudjoao"
        user.project = project
        user.save()
        response = self.client.get("/branches/datecommits/{chat_id}".format(
                                    chat_id=user.chat_id))
        User.delete(user)
        Project.delete(project)
        data = json.loads(response.data.decode())
        date_commits_string = json.dumps(not_found_schema)
        date_commits_json = json.loads(date_commits_string)

        self.assertEqual(response.status_code, 401)
        validate(data, date_commits_json)

    def test_views_date_commits_attribute_error(self):
        GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN", "")
        project = Project()
        project.name = "apitest"
        project.save()
        user = User()
        user.chat_id = "00000"
        user.access_token = GITHUB_API_TOKEN
        user.github_user = "sudjoao"
        user.project = project
        user.save()
        response = self.client.get("/branches/datecommits/{chat_id}".format(
                                    chat_id=None))
        User.delete(user)
        Project.delete(project)
        data = json.loads(response.data.decode())
        date_commits_string = json.dumps(not_found_schema)
        date_commits_json = json.loads(date_commits_string)

        self.assertEqual(response.status_code, 404)
        validate(data, date_commits_json)
