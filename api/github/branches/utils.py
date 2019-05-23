import requests
from requests.exceptions import HTTPError
import json


class Branch():

    def __init__(self, GITHUB_TOKEN):
        self.GITHUB_TOKEN = GITHUB_TOKEN
        self.github_url = "https://api.github.com/repos/"
        self.headers = {"Content-Type": "applications/json",
                        "Authorization": "Bearer " +
                        self.GITHUB_TOKEN}

    def get_branches_names(self, project_name, project_owner):

        try:
            branches_dict = {"branches": []}
            response = requests.get(self.github_url + "{project_owner}/"
                                    "{project_name}/branches".format(
                                        project_owner=project_owner,
                                        project_name=project_name),
                                    headers=self.headers)
            response.raise_for_status()
            received_branches = response.json()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            for i, item in enumerate(received_branches):
                branches_data = {"name": 0}
                branches_data["name"] = received_branches[i]["name"]
                branches_dict["branches"].append(branches_data)
        return branches_dict

    def get_date_last_commit_branches(self,  project_name, project_owner):

        try:
            branches_dict = {"branches": []}
            branches_names = self.get_branches_names(
                             project_name, project_owner)

        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            for i, branch_name in enumerate(branches_names["branches"]):
                branches_data = {"name": 0, "date": 0}
                response = requests.get(self.github_url + "{project_owner}/"
                                        "{project_name}/branches/"
                                        "{branch_name}".format(
                                            project_owner=project_owner,
                                            project_name=project_name,
                                            branch_name=branch_name["name"]),
                                        headers=self.headers)
                received_json = response.json()
                branches_data["name"] = branch_name["name"]
                branches_data["date"] = (received_json["commit"]["commit"]
                                                      ["author"]["date"])
                branches_dict["branches"].append(branches_data)
        return branches_dict
