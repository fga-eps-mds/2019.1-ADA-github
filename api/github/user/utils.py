# api/github/__init__.py

import requests
import sys


class UserInfo():
    def __init__(self, GITHUB_TOKEN):
        self.GITHUB_TOKEN = GITHUB_TOKEN

    def get_user(self):
        headers = {
            "Content-Type": "applications/json",
            "Authorization": "Bearer " + self.GITHUB_TOKEN
        }

        response = requests.get('https://api.github.com/user', headers=headers)
        requested_user = response.json()
        github_data = {"github_username": requested_user["login"],
                       "github_user_id": requested_user["id"]}
        print(github_data, file=sys.stderr)
        return github_data

    def get_repos(self):
        headers = {
            "Content-Type": "applications/json",
            "Authorization": "Bearer " + self.GITHUB_TOKEN
        }
        login = self.get_user()
        response = requests.get("https://api.github.com/users/{login}"
                                "/repos".format(login=login),
                                headers=headers)
        repository = response.json()
        requested_repositories = {"repositories": []}
        for i, item in enumerate(repository):
            repository_data = {"name": 0}
            repository_data["name"] = repository[i]['name']
            requested_repositories["repositories"].append(repository_data)

        return requested_repositories
