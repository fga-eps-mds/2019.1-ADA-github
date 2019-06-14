import json
from github.tests.base import BaseTestCase
from github.tests.jsonschemas.contributor_issues.schemas import\
    get_contributor_issues_schema, get_invalid_contributor_issues_schema,\
    invalid_project_schema
from jsonschema import validate
import os
from github.contributor_issues.utils import ContributorIssues
from unittest.mock import patch
from requests.exceptions import HTTPError
from requests import Response

GITHUB_API_TOKEN = os.environ.get("GITHUB_API_TOKEN", "")


class TestContributorIssues(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.contributor_issues = ContributorIssues(self.user.chat_id)

        self.mocked_get_contributor_issues = Response()
        self.mocked_get_contributor_issues.status_code = 200
        get_contributor_issues_response_content = [{"number": 1,
                                                    "title": "Ada issue test",
                                                    "html_url": "urltest.com"
                                                    }]
        get_contributor_issues_content_in_binary = json.\
            dumps(get_contributor_issues_response_content).encode('utf-8')
        self.mocked_get_contributor_issues._content = \
            get_contributor_issues_content_in_binary

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

    @patch('github.utils.github_utils.get')
    def test_utils_get_contributor_issues(self, mocked_get):
        mocked_get.return_value = self.mocked_get_contributor_issues
        contributor_issues = self.contributor_issues\
            .get_contributor_issues("sudjoao/apitest", "sudjoao")
        self.assertIsInstance(contributor_issues, list)

    @patch('github.utils.github_utils.get')
    def test_utils_invalid_get_contributor_issues(self, mocked_get):
        mocked_get.return_value = self.response_not_found

        with self.assertRaises(HTTPError) as context:
            self.contributor_issues.get_contributor_issues(
                "sudjoao/apitest", "sudjoao")
        notfound_json = json.loads(str(context.exception))
        self.assertEqual(notfound_json["status_code"], 404)
        validate(notfound_json, invalid_project_schema)

    @patch('github.utils.github_utils.get')
    def test_views_get_contributor_issues(self, mocked_get):
        mocked_get.side_effect = (self.mocked_get_project,
                                  self.mocked_get_contributor_issues)
        response = self.client.get("/api/get_contributor_issues/"
                                   "{chat_id}/{contributor_username}".format(
                                            chat_id=self.user.chat_id,
                                            contributor_username="sudjoao"))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, get_contributor_issues_schema)

    @patch('github.utils.github_utils.get')
    def test_views_404_get_contributor_issues(self, mocked_get):
        mocked_get.return_value = self.response_not_found
        response = self.client.get("/api/get_contributor_issues/"
                                   "{chat_id}/{contributor_username}".format(
                                       chat_id=222,
                                       contributor_username="invalid"))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        validate(data, get_invalid_contributor_issues_schema)
