import unittest
from github.tests.base import BaseTestCase
from github.webhook.webhook_utils import Webhook
import os
import json
from github.tests.jsonschemas.webhooks.schemas import\
    set_webhook_schema, not_found_schema,\
    key_error_notificaions_schema
from jsonschema import validate
from unittest.mock import patch, Mock

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "")
GITHUB_API_TOKEN = os.environ.get("GITHUB_API_TOKEN", "")


class TestWebhook(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.webhook = Webhook(self.user.chat_id)
        self.headers = {
            "Content-Type": "applications/json"
        }

    @patch('github.webhook.views.Bot')
    @patch('github.utils.github_utils.post')
    def test_view_delete_hook(self, mocked_post, mocked_bot):
        mocked_bot.return_value = Mock()
        mocked_bot.send_message = Mock()
        mocked_post.response = {}
        user_data = {
            "chat_id": self.user.chat_id,
            "owner": self.user.github_user,
            "repo": self.project.name}
        response = self.client.post("/webhook/delete",
                                    headers=self.headers,
                                    data=json.dumps(user_data))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, set_webhook_schema)

    @patch('github.webhook.views.Bot')
    @patch('github.utils.github_utils.post')
    def test_view_register_user(self, mocked_post, mocked_bot):
        mocked_bot.return_value = Mock()
        mocked_bot.send_message = Mock()
        mocked_post.response = {}
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

    @patch('github.webhook.views.Bot')
    @patch('github.webhook.views.request')
    def test_view_new_comment_issue(self, mocked_request, mocked_bot):
        mocked_bot.return_value = Mock()
        mocked_bot.send_message = Mock()
        mocked_request.json = {
                "action": "created",
                "issue": {
                    "html_url": "https://github.com/Codertocat/Hello-World/"
                                "issues/"
                                "1#issuecomment-492700400",
                    "user": {
                        "login": "Codertocat",
                        "html_url": "https://github.com/Codertocat"
                    },
                    "body": "You are totally right! I'll get this"
                            " fixed right away.",
                    "title": "Spelling error in the README file",
                    "number": 1
                    },
                "comment": {
                    "html_url": "https://github.com/Codertocat/Hello-World/"
                                "issues/"
                                "1#issuecomment-492700400",
                    "body": "You are totally right! I'll get this"
                            " fixed right away."
                    },
                "repository": {
                    "name": "Hello-World"
                }
        }
        response = self.client.post("/github/webhooks/{chat_id}"
                                    .format(chat_id=self.user.chat_id),
                                    headers=self.headers)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, set_webhook_schema)

    @patch('github.webhook.views.Bot')
    @patch('github.webhook.views.request')
    def test_view_new_pull_request(self, mocked_request, mocked_bot):
        mocked_bot.return_value = Mock()
        mocked_bot.send_message = Mock()
        mocked_request.json = {
            "action": "opened",
            "number": 2,
            "pull_request": {
                "url": "https://api.github.com/repos/Codertocat/Hello-World/"
                       "pulls/2",
                "html_url": "https://github.com/Codertocat/Hello-World/pull/2",
                "number": 2,
                "title": "Update the README with new information.",
                "user": {
                    "login": "Codertocat",
                    "html_url": "https://github.com/Codertocat"
                },
                "body": "This is a pretty simple change that we need to pull"
                        " into master.",
                },
            "repository": {
                "name": "Hello-World"
            }
        }
        response = self.client.post("/github/webhooks/{chat_id}"
                                    .format(chat_id=self.user.chat_id),
                                    headers=self.headers)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, set_webhook_schema)

    @patch('github.webhook.views.Bot')
    @patch('github.webhook.views.request')
    def test_view_new_pull_request_comment(self, mocked_request, mocked_bot):
        mocked_bot.return_value = Mock()
        mocked_bot.send_message = Mock()
        mocked_request.json = {
            "action": "submitted",
            "review": {
                "user": {
                    "login": "Codertocat",
                    "html_url": "https://github.com/Codertocat"
                },
                "body": "This is a pretty simple change that we need to pull"
                        " into master.",
                "state": "approved"
                },
            "pull_request": {
                "html_url": "https://github.com/Codertocat/Hello-World/pull/2",
                "title": "Update the README with new information."
            },
            "repository": {
                "name": "Hello-World"
            }
        }
        response = self.client.post("/github/webhooks/{chat_id}"
                                    .format(chat_id=self.user.chat_id),
                                    headers=self.headers)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, set_webhook_schema)

    @patch('github.webhook.views.request')
    @patch('github.webhook.views.request')
    def test_view_new_issue(self, mocked_request, mocked_bot):
        mocked_bot.return_value = Mock()
        mocked_bot.send_message = Mock()
        mocked_request.json = {
            "action": "opened",
            "number": 2,
            "issue": {
                "url": "https://api.github.com/repos/Codertocat/Hello-World"
                       "/pulls/2",
                "html_url": "https://github.com/Codertocat/Hello-World/pull/2",
                "number": 2,
                "title": "Update the README with new information.",
                "body": "You are totally right! I'll get this"
                            " fixed right away.",
                "user": {
                    "login": "Codertocat",
                    "html_url": "https://github.com/Codertocat"
                }
            },
            "repository": {
                "name": "Hello-World"
            }
        }
        response = self.client.post("/github/webhooks/{chat_id}"
                                    .format(chat_id=self.user.chat_id),
                                    headers=self.headers)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, set_webhook_schema)

    @patch('github.webhook.views.request')
    @patch('github.webhook.views.request')
    def test_view_pull_request_review_comment(self, mocked_request,
                                              mocked_bot):
        mocked_bot.return_value = Mock()
        mocked_bot.send_message = Mock()
        mocked_request.json = {
            "action": "created",
            "pull_request_review_comment": "test"
        }
        response = self.client.post("/github/webhooks/{chat_id}"
                                    .format(chat_id=self.user.chat_id),
                                    headers=self.headers)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, set_webhook_schema)

    @patch('github.webhook.views.request')
    @patch('github.webhook.views.request')
    def test_view_review(self, mocked_request, mocked_bot):
        mocked_bot.return_value = Mock()
        mocked_bot.send_message = Mock()
        mocked_request.json = {
            "action": "submitted",
            "review": "test"
        }
        response = self.client.post("/github/webhooks/{chat_id}"
                                    .format(chat_id=self.user.chat_id),
                                    headers=self.headers)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, set_webhook_schema)

    @patch('github.webhook.views.request')
    @patch('github.webhook.views.request')
    def test_view_review_requested(self, mocked_request, mocked_bot):
        mocked_bot.return_value = Mock()
        mocked_bot.send_message = Mock()
        mocked_request.json = {
            "action": "review_requested",
            "number": 2,
            "pull_request": {
                "url": "https://api.github.com/repos/Codertocat/"
                       "Hello-World/pulls/2",
                "html_url": "https://github.com/Codertocat/Hello-World/pull/2",
                "number": 2,
                "title": "Update the README with new information.",
                "user": {
                    "login": "Codertocat",
                    "html_url": "https://github.com/Codertocat"
                },
                "requested_reviewers": [
                    {
                        "login": "Codertocat",
                        "html_url": "https://github.com/Codertocat"
                    }
                ]
            },
            "repository": {
                "name": "Hello-World"
            }
        }
        response = self.client.post("/github/webhooks/{chat_id}"
                                    .format(chat_id=self.user.chat_id),
                                    headers=self.headers)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, set_webhook_schema)

    @patch('github.webhook.views.request')
    def test_view_review_requested_key_error(self, mocked_request):
        mocked_request.json = {
            "action": "review_requested",
            "number": 2,
            "pull_request": {
                "url": "https://api.github.com/repos/Codertocat/"
                       "Hello-World/pulls/2",
                "html_url": "https://github.com/Codertocat/Hello-World/pull/2",
                "number": 2,
                "title": "Update the README with new information.",
                "user": {
                    "login": "Codertocat",
                    "html_url": "https://github.com/Codertocat"
                }
            }
        }
        response = self.client.post("/github/webhooks/{chat_id}"
                                    .format(chat_id=self.user.chat_id),
                                    headers=self.headers)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        validate(data, key_error_notificaions_schema)

    def test_view_register_user_http_error(self):
        self.user.access_token = "wrong_token"
        self.user.save()
        user_data = {
            "chat_id": self.user.chat_id,
            "owner": self.user.github_user}
        response = self.client.post("/webhook",
                                    data=json.dumps(user_data),
                                    headers=self.headers)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        validate(data, not_found_schema)

    def test_view_delete_hook_http_eror(self):
        self.user.access_token = "wrong_token"
        self.user.save()
        data = {
            "chat_id": self.user.chat_id,
            "owner": self.user.github_user,
            "repo": self.project.name}
        response = self.client.post("/webhook/delete",
                                    headers=self.headers,
                                    data=json.dumps(data))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        validate(data, not_found_schema)


if __name__ == "__main__":
    unittest.main()
