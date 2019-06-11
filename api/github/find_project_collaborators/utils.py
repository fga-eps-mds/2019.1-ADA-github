from github.utils.github_utils import GitHubUtils


class FindProjectCollaborators(GitHubUtils):

    def __init__(self, chat_id):
        super().__init__(chat_id)

    def get_project(self, project_name):
        url = self.GITHUB_API_URL + "user/repos"
        repositories = self.request_url(url, "get")
        for item in repositories:
            if(item["name"] == project_name):
                owner_and_repo = item["full_name"]
                break
        return owner_and_repo

    def get_collaborators(self, owner_and_repo):
        url = self.GITHUB_API_URL + "repos/{owner_repo}/contributors"\
                                    .format(owner_repo=owner_and_repo)
        contributors_informations = self.request_url(url, "get")
        contributors_names = []
        for item in contributors_informations:
            contributors_names.append(item["login"])

        return contributors_names
