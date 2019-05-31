import requests
from requests.exceptions import HTTPError
import json

class ContributorIssues():

    def __init__(self, GITHUB_TOKEN):
        self.GITHUB_TOKEN = GITHUB_TOKEN

    def get_contributor_issues(self, repo_fullname ,contributor_name):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITHUB_TOKEN
        }

        try:
            response = requests.get(
                "https://api.github.com/repos/{repo_fullname}"
                "/issues?assignee={contributor_name}"
                .format(repo_fullname=repo_fullname,
                 contributor_name=contributor_name),
                 headers=headers)
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            issues_info = [{}]
            repo_issues = response.json()
            for issue_info in repo_issues:
                issues_info.append({
                    "title": issue_info["title"],
                    "url": issue_info["url"],
                    "issue_number": issue_info["number"]
                })
            return issues_info
            


