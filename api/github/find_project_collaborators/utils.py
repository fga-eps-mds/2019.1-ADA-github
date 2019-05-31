import requests
import json
from requests.exceptions import HTTPError


class FindProjectCollaborators():

    def __init__(self, GITHUB_TOKEN):
        self.GITHUB_TOKEN = GITHUB_TOKEN

    def get_project(self, project_name):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITHUB_TOKEN
        }
        try:
            response = requests.get(
                "https://api.github.com/user/repos",
                 headers=headers)

            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))

        else:
            repositories = response.json()
            for item in repositories:
                if(item["name"]==project_name):
                    owner_and_repo = item["full_name"]
                    break

        return owner_and_repo

    def get_collaborators(self, owner_and_repo):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITHUB_TOKEN
        }
        try:

            response = requests.get("https://api.github.com/repos/\
                                     {owner_and_repo}/contributors".
                                     format(owner_and_repo=owner_and_repo),
                                     headers=headers)
            response.raise_for_status()

        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))

        else:
            contributors_informations = response.json()
            contributors_names = []
            for item in contributors_informations:
                contributors_names.append(item["login"])

            return contributors_names
