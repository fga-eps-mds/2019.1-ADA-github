import requests
from requests.exceptions import HTTPError
import json


class Release():

    def __init__(self, GITHUB_TOKEN):
        self.GITHUB_TOKEN = GITHUB_TOKEN
        self.github_url = "https://api.github.com/repos/"
        self.headers = {"Content-Type": "applications/json",
                        "Authorization": "Bearer " +
                        self.GITHUB_TOKEN}

    def get_last_release(self, project_owner, project_name):

        try:
            release_dict = {"release": []}
            release_data = {"name": 0, "body": 0, "created_at": 0}
            response = requests.get(self.github_url + "{project_owner}/"
                                    "{project_name}/releases".format(
                                        project_owner=project_owner,
                                        project_name=project_name),
                                    headers=self.headers)
            response.raise_for_status()
            received_releases = response.json()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            release_data["name"] = received_releases[0]["name"]
            release_data["body"] = received_releases[0]["body"]
            release_data["created_at"] = received_releases[0]["created_at"]
            release_dict["release"].append(release_data)
        return release_dict
