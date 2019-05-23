import requests
import sys


class PullRequest():
    def __init__(self, GITHUB_TOKEN):
        self.GITHUB_TOKEN = GITHUB_TOKEN
        self.github_url = "https://api.github.com/repos/"

    def get_pull_requests(self, project_owner, project_name):
        pull_request_dict = {"pull_request": []}
        pull_request_data = {"title": 0, "url": 0}
        print(pull_request_dict, file=sys.stderr)
        headers = {
            "Content-Type": "applications/json",
            "Authorization": "Bearer " + self.GITHUB_TOKEN
        }
        response = requests.get(self.github_url + "{project_owner}"
                                "/{project_name}/pulls".format(
                                    project_owner=project_owner,
                                    project_name=project_name),
                                headers=headers)
        requested_pull_requests = response.json()

        for i, item in enumerate(requested_pull_requests):
            pull_request_data["title"] = requested_pull_requests[i]["title"]
            pull_request_data["url"] = requested_pull_requests[i]["html_url"]
            pull_request_dict["pull_request"].append(pull_request_data)
        return pull_request_dict
