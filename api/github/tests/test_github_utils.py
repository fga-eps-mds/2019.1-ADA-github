import unittest
from github.tests.base import BaseTestCase
from github.utils.github_utils import GitHubUtils


class TestGithubUtils(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.github_utils = GitHubUtils(self.user.chat_id)

    # def test_request_url_attribute_error(self):
    #     with self.assertRaises(AttributeError) as context:
    #         self.github_utils.request_url(
    #                 self.github_utils.GITHUB_API_URL, None)
    #     notfound_json = json.loads(str(context.exception))
    #     self.assertEqual(notfound_json["status_code"], 404)
    #     validate(notfound_json, invalid_project_schema)

    def test_get_class_type(self):
        test_variable = 5
        test_type = self.github_utils.get_class_type(test_variable)
        expected_response = "classint"
        self.assertEqual(test_type, expected_response)


if __name__ == "__main__":
    unittest.main()
