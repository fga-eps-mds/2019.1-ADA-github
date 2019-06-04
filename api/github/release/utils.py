from github.utils.github_utils import GitHubUtils


class Release(GitHubUtils):

    def __init__(self, chat_id, project_owner, project_name):
        super().__init__(chat_id)
        self.project_owner_project_name = "repos/{project_owner}/"\
                                          "{project_name}".format(
                                           project_owner=project_owner,
                                           project_name=project_name)

    def get_last_release(self):
        url = self.GITHUB_API_URL + self.project_owner_project_name +\
                                    "/releases"
        requested_release = self.request_url(url, "get")
        project_releases = self.releases_requested_releases(requested_release)
        return project_releases

    def releases_requested_releases(self, resp):
        release_dict = {"release": []}
        release_data = {"name": 0, "body": 0, "created_at": 0, "url": 0}
        if resp:
            release_data["name"] = resp[0]["name"]
            release_data["body"] = resp[0]["body"]
            release_data["created_at"] = resp[0]["created_at"]
            release_data["url"] = resp[0]["html_url"]
            release_dict["release"].append(release_data)
        return release_dict
