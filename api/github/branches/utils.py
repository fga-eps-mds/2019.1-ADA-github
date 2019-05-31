from github.utils.github_utils import GitHubUtils
import datetime
from datetime import date


class Branch(GitHubUtils):

    def init(self, chat_id):
        super().init(chat_id)

    def get_branches_names(self, project_owner, project_name):
        url = self.GITHUB_API_URL + self.project_owner_project_name(
                                    project_owner, project_name, "branches")
        requested_branches = self.get_request(url)
        project_branches = self.branches_requested_branches(requested_branches)
        return project_branches

    def get_date_last_commit_branches(self,  project_name, project_owner):
        branches_dict = {"branches": []}
        branches_names = self.get_branches_names(
                            project_name, project_owner)
        for i, branch_name in enumerate(branches_names["branches"]):
            branches_data = {"name": 0, "last_commit_days": 0}
            url = self.GITHUB_API_URL + "repos/{project_owner}/"\
                                        "{project_name}/branches/"\
                                        "{branch_name}".format(
                                            project_owner=project_owner,
                                            project_name=project_name,
                                            branch_name=branch_name["name"])
            requested_dates = self.get_request(url)
            branches_data["name"] = branch_name["name"]
            commit_days = self.get_last_commit_days(
                                        requested_dates["commit"]
                                        ["commit"]["author"]["date"])
            branches_data["last_commit_days"] = commit_days
            branches_dict["branches"].append(branches_data)
        return branches_dict

    def get_last_commit_days(self, branch_commit_date):
        todays_date = date.today()
        commit_date = datetime.datetime.strptime(
            branch_commit_date[0:10], "%Y-%m-%d")
        commit_date = commit_date.date()
        qntd_days = todays_date-commit_date
        commit_days = str(qntd_days.days)
        return commit_days

    def branches_requested_branches(self, resp):
        branches_dict = {"branches": []}
        for i, item in enumerate(resp):
            branches_data = {"name": 0}
            self.update_branches_data(branches_data, branches_dict, resp, i)
        return branches_dict

    def update_branches_data(self, branches_data, branches_dict,
                             resp, count):
        branches_data["name"] = resp[count]["name"]
        branches_dict["branches"].append(branches_data)
