import json
import unittest
from github.tests.base import BaseTestCase
from github.tests.jsonschemas.branches.schemas import\
    ping_schema, valid_schema, unauthorized_schema,\
    valid_branches_names_schema
from jsonschema import validate
from github.branches.utils import Branch
from github.data.user import User
from github.data import init_db
from github.data.project import Project
import os


class TestBranches(BaseTestCase):
    def setup(self):
        init_db()
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
