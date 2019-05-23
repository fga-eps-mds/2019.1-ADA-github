import requests
from requests.exceptions import HTTPError
import json


class PullRequest():
    def __init__(self, GITHUB_TOKEN):
        self.GITHUB_TOKEN = GITHUB_TOKEN
        self.github_url = "https://api.github.com/repos/"
        self.headers = {"Content-Type": "applications/json",
                        "Authorization": "Bearer " +
                        self.GITHUB_TOKEN}

    def get_pull_requests(self, project_owner, project_name):
        try:
            pull_request_dict = {"pull_request": []}

            response = requests.get(self.github_url + "{project_owner}"
                                    "/{project_name}/pulls".format(
                                        project_owner=project_owner,
                                        project_name=project_name),
                                    headers=self.headers)
            requested_pull_requests = response.json()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            for i, data in enumerate(requested_pull_requests):
                pull_request_data = {"title": 0, "url": 0}
                pull_request_data["title"] = data["title"]
                pull_request_data["url"] = data["html_url"]
                pull_request_dict["pull_request"].append(pull_request_data)
        return pull_request_dict
