import json
from github.tests.base import BaseTestCase
from github.tests.jsonschemas.release.schemas import\
    not_found_schema, valid_release_schema,\
    invalid_project_schema
from jsonschema import validate
from github.release.utils import Release
from requests.exceptions import HTTPError


class TestRelease(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.release = Release(self.user.chat_id,
                               self.user.github_user,
                               self.project.name)

    def test_utils_get_last_release(self):
        releases_data = self.release.get_last_release()
        validate(releases_data, valid_release_schema)

    def test_utils_get_last_release_invalid_username(self):
        project_owner = "wrong_user"
        wrong_release = Release(self.user.chat_id,
                                project_owner,
                                self.project.name)
        with self.assertRaises(HTTPError) as context:
            wrong_release.get_last_release()
        notfound_json = json.loads(str(context.exception))
        self.assertEqual(notfound_json["status_code"], 404)
        validate(notfound_json, invalid_project_schema)

    def test_views_get_releases_request(self):
        response = self.client.get("/release/{chat_id}".format(
                                    chat_id=self.user.chat_id))
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        validate(data, valid_release_schema)

    def test_views_get_releases_invalid_username(self):
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
