from github.utils.github_utils import GitHubUtils


class Issue(GitHubUtils):

    def __init__(self, chat_id):
        super().__init__(chat_id)

    def create_issue(self, repository_name, username, title, body):

        data = {
                "title": title,
                "body": body,
                "assignees": [
                    username
                    ]
               }

        url = self.GITHUB_API_URL + "repos/{username}/"\
                                    "{repository_name}/issues".format(
                                        username=username,
                                        repository_name=repository_name)

        requested_issue = self.request_url(url, "post", data)
        issue_dict = {"title": requested_issue["title"],
                      "body": requested_issue["body"],
                      "html_url": requested_issue["html_url"]}
        return issue_dict

    def comment_issue(self, repository_name, username, issue_number, body):

        data = {
                "body": body
               }

        url = self.GITHUB_API_URL + "repos/{username}/"\
                                    "{repository_name}/issues/"\
                                    "{issue_number}/comments".format(
                                        username=username,
                                        repository_name=repository_name,
                                        issue_number=issue_number)

        requested_comment_issue = self.request_url(url, "post", data)
        comment_issue_dict = {
                              "body": requested_comment_issue["body"]
                             }
        return comment_issue_dict
