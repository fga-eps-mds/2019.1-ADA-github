# api/github/__init__.py

import requests
from requests.exceptions import HTTPError
import json


class Issue():
    def __init__(self, GITHUB_API_TOKEN):
        self.GITHUB_API_TOKEN = GITHUB_API_TOKEN

    def get_list_issues(self, project_org, project_name):
        response = requests.get(
            "https://api.github.com/orgs/:org/issues")
    def create_issue():
        response = requests.get(
            "https://api.github.com/orgs/:org/issues")

