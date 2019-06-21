from requests import delete
import os
from github.utils.github_utils import GitHubUtils


GITHUB_SERVICE_URL = os.environ.get("GITHUB_SERVICE_URL", "")
WEBHOOK_URL_ENVIRONMENT = os.getenv("WEBHOOK_URL_ENVIRONMENT", "")


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
            user_hooks_url = WEBHOOK_URL_ENVIRONMENT
            for user_hooks in hook:
                if user_hooks_url in user_hooks["config"]["url"]:
                    hook_id = user_hooks["id"]
            delete_hook_url = "https://api.github.com/"\
                              "repos/{owner}/{repo}/"\
                              "hooks/{hook_id}".format(owner=owner,
                                                       repo=repo,
                                                       hook_id=hook_id)
            req = delete(delete_hook_url, headers=self.headers)
            req.raise_for_status()

    def get_message_info(self, req_json):
        dict_message = {
            "user": 0,
            "user_url": 0,
            "title": 0,
            "number": 0,
            "repo_name": 0,
            "url": 0,
            "body": 0,
        }
        if "review" in list(req_json.keys()):
            key = "review"
            dict_message = self.update_message_keys(key, req_json,
                                                    dict_message)
        elif "pull_request" in list(req_json.keys()):
            key = "pull_request"
            dict_message = self.update_message_keys(key, req_json,
                                                    dict_message)
        elif "issue" in list(req_json.keys()):
            key = "issue"
            dict_message = self.update_message_keys(key, req_json,
                                                    dict_message)
        return dict_message

    def update_message_keys(self, key, req_json, dict_message):
        dict_message["user"] = req_json[key]["user"]["login"]
        dict_message["user_url"] = req_json[key]["user"]["html_url"]
        dict_message["body"] = req_json[key]["body"]
        if(key == "review"):
            dict_message["title"] = req_json["pull_request"]["title"]
            dict_message["url"] = req_json["pull_request"]["html_url"]
            return dict_message
        dict_message["title"] = req_json[key]["title"]
        dict_message["number"] = req_json[key]["number"]
        dict_message["url"] = req_json[key]["html_url"]
        dict_message["repo_name"] = req_json["repository"]["name"]
        return dict_message

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
                            [0]["login"])
        reviewer_message = "["+reviewer+"]"
        return reviewer_message

    def get_body_and_body_url(self, req_json):
        url = req_json["comment"]["html_url"]
        body = req_json["comment"]["body"]
        return url, body
