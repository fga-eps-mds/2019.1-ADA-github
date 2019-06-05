import unittest
from github.tests.base import BaseTestCase
from github.webhook.webhook_utils import Webhook
import os
import json
from github.tests.jsonschemas.webhooks.schemas import\
    set_webhook_schema, not_found_schema
from jsonschema import validate
# from github.tests.jsonschemas.webhooks.webhook_jsons import\
#     issue_comment

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "")
GITHUB_API_TOKEN = os.environ.get("GITHUB_API_TOKEN", "")


class TestWebhook(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.webhook = Webhook(self.user.chat_id)
        self.headers = {
            "Content-Type": "applications/json"
        }

    def test_view_delete_hook(self):
        data = {
            "chat_id": self.user.chat_id,
            "owner": self.user.github_user,
            "repo": self.project.name}
        response = self.client.post("/webhook/delete",
                                    headers=self.headers,
                                    data=json.dumps(data))
        self.assertEqual(response.status_code, 200)

    def test_view_register_user(self):
        user_data = {
            "chat_id": self.user.chat_id,
            "owner": self.user.github_user,
            "repo": self.project.name}
        response = self.client.post("/webhook",
                                    data=json.dumps(user_data),
                                    headers=self.headers)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, set_webhook_schema)

    # def test_view_register_user_none_chat_id(self):
    #     user_data = {
    #         "chat_id": None,
    #         "owner": self.user.github_user,
    #         "repo": self.project.name}
    #     response = self.client.post("/webhook",
    #                                 data=json.dumps(user_data),
    #                                 headers=self.headers)
    #     data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 404)
    #     validate(data, set_webhook_schema)

    def test_view_register_user_no_repo(self):
        user_data = {
            "chat_id": self.user.chat_id,
            "owner": self.user.github_user}
        response = self.client.post("/webhook",
                                    data=json.dumps(user_data),
                                    headers=self.headers)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        validate(data, not_found_schema)

    # def test_view_new_comment_issue(self):
    #     response = self.client.post("/github/webhooks/{chat_id}"
    #                                 .format(chat_id=self.user.chat_id),
    #                                 data=json.dumps(issue_comment),
    #                                 headers=self.headers)
    #     data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 200)
    #     validate(data, set_webhook_schema)

    # def test_webhook(self):
    #     data = {
    #         "chat_id": "367302295",
    #         "owner": "sudjoao",
    #         "repo": "apitest"
    #     }
    #     headers = {
    #         "Content-Type": "applications/json"
    #     }
    #     response = self.client.post("/webhook",
    #                                 headers=headers,
    #                                 data=json.dumps(data))
    #     self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
