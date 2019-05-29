import requests
import json
from github.data.user import User
import os

GITHUB_SERVICE_URL = os.environ.get("GITHUB_SERVICE_URL", "")


class Webhook():
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self. webhook_json = {
            "name": "web",
            "config": {
                "url": GITHUB_SERVICE_URL + "github/webhooks/{chat_id}"
                                            .format(chat_id=self.chat_id),
                "content_type": "json",
                "insecure_ssl": "1"
            },
            "events": ["pull_request_review",
                       "issues",
                       "pull_request"],
            "active": True
        }

    def set_webhook(self, owner, repo):
        set_webhook_url = "https://api.github.com/"\
                          "repos/{owner}/{repo}/"\
                          "hooks".format(owner=owner,
                                         repo=repo)
        user = User.objects(chat_id=self.chat_id).first()
        GITHUB_TOKEN = user.access_token
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + GITHUB_TOKEN
        }
        requests.post(url=set_webhook_url,
                      data=json.dumps(self.webhook_json),
                      headers=headers)
