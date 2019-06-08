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
        self.request_url(set_webhook_url, "post", self.webhook_json)

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

    def get_message_info(self, req_json):
        if "pull_request" in list(req_json.keys()):
            key = "pull_request"
        elif "issue" in list(req_json.keys()):
            key = "issue"
        else:
            return None, None, None, None, None
        user = req_json[key]["user"]["login"]
        user_url = req_json[key]["user"]["html_url"]
        title = req_json[key]["title"]
        number = req_json[key]["number"]
        repo_name = req_json["repository"]["name"]
        return user, user_url, title, number, repo_name

    def get_post_info(self, post_json):
        dict_infos = {
            "chat_id": post_json["chat_id"],
            "owner": post_json["owner"],
            "repo": post_json["repo"]
        }
        return dict_infos

    def get_reviewer_login(self, req_json):
        reviewer = (req_json["pull_request"]
                            ["requested_reviewers"]
                            [0]["html_url"])
        reviewer_message = "("+reviewer+")"
        return reviewer_message

    def get_body_and_body_url(self, req_json):
        url = req_json["comment"]["html_url"]
        body = req_json["comment"]["body"]
        return url, body
