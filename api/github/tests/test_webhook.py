
import unittest
from github.data.user import User
from github.tests.base import BaseTestCase
import os
import json

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "")
GITHUB_API_TOKEN = os.environ.get("GITHUB_API_TOKEN", "")


class TestWebhook(BaseTestCase):
    def setUp(self):
        super().setUp()
        User.drop_collection()
        self.user = User()
        self.user.access_token = str(GITHUB_API_TOKEN)
        self.user.github_user = "joaovitor3"
        self.user.chat_id = '367302295'
        self.user.save()

    def test_delete_hook(self):
        data = {
            "chat_id": "367302295",
            "owner": "sudjoao",
            "repo": "apitest"
        }
        headers = {
            "Content-Type": "applications/json"
        }
        response = self.client.post("/webhook/delete",
                                    headers=headers,
                                    data=json.dumps(data))
        self.assertEqual(response.status_code, 200)

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
