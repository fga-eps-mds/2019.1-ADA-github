import requests
from requests.exceptions import HTTPError
import json


class Issue():

    def __init__(self, GITHUB_TOKEN):
        self.GITHUB_TOKEN = GITHUB_TOKEN

    def create_issue(self, repository_name, username, title, body):

        data = {
                "title": title,
                "body": body,
                "assignees": [
                    username
                    ]
               }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITHUB_TOKEN
        }
        try:
            response = requests.post(
                "https://api.github.com/repos/{username}/"
                "{repository_name}/issues".format(username=username,
                                                  repository_name=(
                                                      repository_name)),
                data=json.dumps(data),
                headers=headers)
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            created_issue = response.json()
            issue_dict = {"title": created_issue["title"],
                          "body": created_issue["body"],
                          "html_url": created_issue["html_url"]}
            return issue_dict
