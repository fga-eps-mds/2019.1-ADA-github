import requests
from requests.exceptions import HTTPError
import json


class Issue():

    def __init__(self, GITHUB_API_TOKEN):
        self.GITHUB_API_TOKEN = GITHUB_API_TOKEN

    # def get_list_issues(self, project_org, project_name):
    #     response = requests.get(
    #         "https://api.github.com/orgs/:org/issues")

    def get_github_username(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITHUB_API_TOKEN
        }
        try:
            response = requests.get("https://api.github.com/user",
                                    headers=headers)
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            username = response.json()
            return username["login"]

    def create_issue(self, repository_name):

        username = self.get_github_username()
        title = "Found a bug"
        body = "I'm having a problem with this."
        # assignees = ["caiovfernandes"]

        data = {
                "title": title,
                "body": body,
                "assignees": [
                    "sudjoao"
                    ]
               }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITHUB_API_TOKEN
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
            return created_issue
