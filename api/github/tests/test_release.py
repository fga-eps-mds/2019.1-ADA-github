import json
from github.tests.base import BaseTestCase
from github.tests.jsonschemas.release.schemas import\
    not_found_schema, valid_release_schema,\
    invalid_project_schema
from jsonschema import validate
from github.release.utils import Release
from requests.exceptions import HTTPError
from requests import Response
from unittest.mock import patch


class TestRelease(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.release = Release(self.user.chat_id,
                               self.user.github_user,
                               self.project.name)
        self.mocked_valid_response = Response()
        mocked_release_content = [
            {
                "name": "v1",
                "body": "teste",
                "created_at": "12-12-2019",
                "html_url": "www.google.com"
            }]
        content_release_binary = json.dumps(mocked_release_content).\
            encode('utf-8')
        self.mocked_valid_response._content = content_release_binary
        self.mocked_valid_response.status_code = 200

    @patch('github.utils.github_utils.get')
    def test_utils_get_last_release(self, mocked_get):
        mocked_get.return_value = self.mocked_valid_response
        releases_data = self.release.get_last_release()
        validate(releases_data, valid_release_schema)

    @patch('github.utils.github_utils.get')
    def test_utils_get_last_release_invalid_username(self, mocked_get):
        mocked_get.return_value = self.response_not_found
        project_owner = "wrong_user"
        wrong_release = Release(self.user.chat_id,
                                project_owner,
                                self.project.name)
        with self.assertRaises(HTTPError) as context:
            wrong_release.get_last_release()
        notfound_json = json.loads(str(context.exception))
        self.assertEqual(notfound_json["status_code"], 404)
        validate(notfound_json, invalid_project_schema)

    @patch('github.utils.github_utils.get')
    def test_views_get_releases_request(self, mocked_get):
        mocked_get.return_value = self.mocked_valid_response
        response = self.client.get("/release/{chat_id}".format(
                                    chat_id=self.user.chat_id))
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        validate(data, valid_release_schema)

    @patch('github.utils.github_utils.get')
    def test_views_get_releases_invalid_username(self, mocked_get):
        mocked_get.return_value = self.response_not_found
        self.user.github_user = "wrong_user"
        self.user.save()
        response = self.client.get("/release/{chat_id}".format(
                                    chat_id=self.user.chat_id))
        data = json.loads(response.data.decode())
        release_string = json.dumps(not_found_schema)
        release_json = json.loads(release_string)
        self.assertEqual(response.status_code, 404)
        validate(data, release_json)

    def test_views_get_releases_attribute_error(self):
        response = self.client.get("/release/{chat_id}".format(
                                    chat_id=None))
        data = json.loads(response.data.decode())
        release_string = json.dumps(not_found_schema)
        release_json = json.loads(release_string)
        self.assertEqual(response.status_code, 404)
        validate(data, release_json)
