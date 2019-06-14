from github.utils.github_utils import GitHubUtils


class PullRequest(GitHubUtils):

    def __init__(self, chat_id):
        super().__init__(chat_id)

    def get_pull_requests(self, project_owner, project_name):
        url = self.GITHUB_API_URL + "repos/{project_owner}"\
                                    "/{project_name}/pulls".format(
                                     project_owner=project_owner,
                                     project_name=project_name)
        requested_pull_requests = self.request_url(url, "get")
        project_pull_request = self.pull_requested_pull(
                                    requested_pull_requests)
        return project_pull_request

    def pull_requested_pull(self, resp):
        pull_request_dict = {"pull_request": []}
        for i, data in enumerate(resp):
            pull_request_data = {"title": 0, "url": 0}
            pull_request_data["title"] = data["title"]
            pull_request_data["url"] = data["html_url"]
            pull_request_dict["pull_request"].append(pull_request_data)
        return pull_request_dict

    def create_pull_request(self, repository_name, title,
                            body, username, head, base):

        data = {
                "title": title,
                "body": body,
                "head": head,
                "base": base
        }

        url = self.GITHUB_API_URL + "repos/{username}/{repository_name}"\
                                    "/pulls".format(
                                            username=username,
                                            repository_name=repository_name)
        requested_pull_request = self.request_url(url, "post", data)
        pr_dict = {"title": requested_pull_request["title"],
                   "body": requested_pull_request["body"],
                   "head": requested_pull_request["head"],
                   "base": requested_pull_request["base"]}
        return pr_dict
