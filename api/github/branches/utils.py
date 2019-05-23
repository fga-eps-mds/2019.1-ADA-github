import requests
import sys


class Branch():

    def __init__(self, GITHUB_TOKEN):
        self.GITHUB_TOKEN = GITHUB_TOKEN
        self.github_url = "https://api.github.com/repos/"

    def get_branches_names(self, project_name, project_owner):
        headers = {
            "Content-Type": "applications/json",
            "Authorization": "Bearer " + self.GITHUB_TOKEN
        }
        response = requests.get(self.github_url+"{project_owner}/"
                                "{project_name}/branches".format(
                                    project_owner=project_owner,
                                    project_name=project_name),
                                headers=headers)
        response.raise_for_status()
        received_branches = response.json()
        branches = {"name": []}
        for i, item in enumerate(received_branches):
            branches["name"].append(received_branches[i]["name"])
        return branches

    def get_date_last_commit_branches(self,  project_name, project_owner):
        headers = {
            "Content-Type": "applications/json",
            "Authorization": "Bearer " + self.GITHUB_TOKEN
         }
        branches_names = self.get_branches_names(project_name, project_owner)
        branches = {"name": [], "date": []}
        for branch_name in branches_names["name"]:
            print(branch_name, file=sys.stderr)
            response = requests.get(self.github_url+"{project_owner}/"
                                    "{project_name}/branches/"
                                    "{branch_name}".format(
                                            project_owner=project_owner,
                                            project_name=project_name,
                                            branch_name=branch_name),
                                    headers=headers)
            received_json = response.json()
            branches["name"].append(branch_name)
            branches["date"].append((received_json["commit"]["commit"]
                                                  ["author"]["date"]))
        return branches
