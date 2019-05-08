# api/github/__init__.py

import requests
import sys
from requests.exceptions import HTTPError
import json


class User():
    def __init__(self, GITHUB_TOKEN):
        self.GITHUB_TOKEN = GITHUB_TOKEN

    def get_user(self):
        headers = {
            "Content-Type": "applications/json",
            "Authorization": "Bearer " + self.GITHUB_TOKEN
        }

        response = requests.get('https://api.github.com/user', headers=headers)
        requested_user = response.json()
        return requested_user['login']

    def get_repos(self):
        headers = {
            "Content-Type": "applications/json",
            "Authorization": "Bearer " + self.GITHUB_TOKEN
        }
        login = self.get_user()
        response = requests.get('https://api.github.com/users/{login}/repos'.format(login=login), 
                                headers=headers)
        repos = response.json()
        requested_repos = []
        for i, item in enumerate(repos):
            repo_data = {"repository": 0}
            repo_data["repository"] = repos[i]['name']
            requested_repos.append(repo_data)
        
        return requested_repos

