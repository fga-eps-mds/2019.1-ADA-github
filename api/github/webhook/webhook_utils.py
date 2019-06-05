import requests
import os
from github.utils.github_utils import GitHubUtils
GITHUB_SERVICE_URL = os.environ.get("GITHUB_SERVICE_URL", "")


class Webhook(GitHubUtils):
    def __init__(self, chat_id):
        super().__init__(chat_id)
        self.chat_id = chat_id
        self. webhook_json = {
            "name": "web",
            "config": {
                "url": GITHUB_SERVICE_URL + "github/webhooks/{chat_id}"
                                            .format(chat_id=self.chat_id),
                "content_type": "json",
                "insecure_ssl": "0"
            },
            "events": ["issue_comment",
                       "issues",
                       "pull_request",
                       "pull_request_review_comment",
                       "pull_request_review"],
            "active": True
        }

    def set_webhook(self, owner, repo):
        set_webhook_url = self.GITHUB_API_URL + \
            "repos/{owner}/{repo}/hooks".format(owner=owner, repo=repo)
        self.request_url(set_webhook_url, "post",
                         self.webhook_json)

    def delete_hook(self, owner, repo):
        hook_url = self.GITHUB_API_URL + "repos/{owner}/{repo}/"\
                   "hooks".format(owner=owner, repo=repo)
        hook = self.request_url(hook_url, "get")
        if len(hook):
            hook_id = hook[0]["id"]
            delete_hook_url = "https://api.github.com/"\
                              "repos/{owner}/{repo}/"\
                              "hooks/{hook_id}".format(owner=owner,
                                                       repo=repo,
                                                       hook_id=hook_id)
            req = requests.delete(delete_hook_url, headers=self.headers)
            req.raise_for_status()
