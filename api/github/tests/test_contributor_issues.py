import json
from github.tests.base import BaseTestCase
from github.tests.jsonschemas.contributor_issues.schemas import\
    get_contributor_issues_schema, get_invalid_contributor_issues_schema
from jsonschema import validate
import os
from github.contributor_issues.utils import ContributorIssues
from unittest.mock import patch
from requests import Response

GITHUB_API_TOKEN = os.environ.get("GITHUB_API_TOKEN", "")


class TestContributorIssues(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.contributor_issues = ContributorIssues(self.user.chat_id)

        self.mocked_get_contributor_issues = Response()
        self.mocked_get_contributor_issues.status_code = 200
        get_contributor_issues_response_content = [{"issue_number": 1,
                                                    "title": "Ada issue test",
                                                    "url": "urltest.com"
                                                    }]
        get_contributor_issues_content_in_binary = json.\
            dumps(get_contributor_issues_response_content).encode('utf-8')
        self.mocked_get_contributor_issues_response = \
            get_contributor_issues_content_in_binary

        self.mocked_invalid_get_contributor_issues = Response()
        self.mocked_invalid_get_contributor_issues.status_code = 404
        get_invalid_contributor_issues_response_content = []
        get_invalid_contributor_issues_content_in_binary = json.\
            dumps(get_invalid_contributor_issues_response_content)\
            .encode('utf-8')
        self.mocked_get_invalid_contributor_issues_response = \
            get_invalid_contributor_issues_content_in_binary

    @patch('github.contributor_issues.utils')
    def test_utils_get_contributor_issues(self, mocked_get):
        mocked_get.return_value = self.mocked_get_contributor_issues_response
        contributor_issues = self.contributor_issues\
            .get_contributor_issues("sudjoao/apitest", "sudjoao")
        self.assertIsInstance(contributor_issues, list)

    @patch('github.contributor_issues.utils')
    def test_utils_invalid_get_contributor_issues(self, mocked_get):
        mocked_get.return_value = self\
            .mocked_get_invalid_contributor_issues_response
        contributor_issues = self.contributor_issues\
            .get_contributor_issues("sudjoao/apitest", "sudjoao")
        self.assertIsInstance(contributor_issues, list)

    @patch('github.contributor_issues.utils')
    def test_views_get_contributor_issues(self, mocked_get):
        mocked_get.return_value = self.mocked_get_contributor_issues_response
        response = self.client.get("/api/get_contributor_issues/"
                                   "{chat_id}/{contributor_username}".format(
                                            chat_id=self.user.chat_id,
                                            contributor_username="sudjoao"))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, get_contributor_issues_schema)

    @patch('github.contributor_issues.utils')
    def test_views_404_get_contributor_issues(self, mocked_get):
        mocked_get.return_value = self.\
            mocked_get_invalid_contributor_issues_response
        response = self.client.get("/api/get_contributor_issues/"
                                   "{chat_id}/{contributor_username}".format(
                                       chat_id=222,
                                       contributor_username="invalid"))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        validate(data, get_invalid_contributor_issues_schema)
