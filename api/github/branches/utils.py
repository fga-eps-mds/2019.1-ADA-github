import requests
import sys
from requests.exceptions import HTTPError
import json
from github.branches.error_messages import UNAUTHORIZED, NOT_FOUND


class Branch():
    def __init__(self, GITHUB_TOKEN):
        self.GITHUB_TOKEN = GITHUB_TOKEN
   
    def get_branches_names(self, project_name, project_owner):
        headers = {
            "Content-Type": "applications/json",
            "Authorization": "Bearer " + self.GITHUB_TOKEN
        }
        response = requests.get("https://api.github.com/repos/"
                                "{project_owner}/{project_name}"
                                "/branches".format(
                                    project_owner=project_owner,
                                    project_name=project_name),
                                headers=headers)
        response.raise_for_status()
        received_branches = response.json()
        branches_names = []
        for i, item in enumerate(received_branches):
            branches_names.append(received_branches[i]["name"])
        return branches_names
