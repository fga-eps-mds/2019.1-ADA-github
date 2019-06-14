from github.utils.github_utils import GitHubUtils


class ContributorIssues(GitHubUtils):

    def __init__(self, chat_id):
        super().__init__(chat_id)

    def get_contributor_issues(self, repo_fullname, contributor_name):

        url = self.GITHUB_API_URL + "repos/{repo_fullname}"\
              "/issues?assignee={contributor_name}"\
              .format(repo_fullname=repo_fullname,
                      contributor_name=contributor_name)
        repo_issues = self.request_url(url, "get")
        issues_info = []
        for issue_info in repo_issues:
            issues_info.append({
                "title": issue_info["title"],
                "url": issue_info["html_url"],
                "issue_number": issue_info["number"]
            })
        return issues_info
