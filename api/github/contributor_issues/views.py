from flask import jsonify, Blueprint, request
from flask_cors import CORS
from github.contributor_issues.utils import ContributorIssues
import json
from github.issue.error_messages import NOT_FOUND, UNAUTHORIZED
from requests.exceptions import HTTPError
from github.data.user import User
from github.data.project import Project

contributor_issues_blueprint = Blueprint("contributor_issues", __name__)
CORS(contributor_issues_blueprint)

@contributor_issues_blueprint.route("/api/get_contributor_issues/<chat_id>/"
                        "<contributor_username>", methods=["GET"])
def get_contributor_issues(chat_id, contributor_username):
    user = User.objects(chat_id=chat_id).first()
    project = user.project
    repo_fullname = "fga-eps-mds/2019.1-ADA"
    contributor_issues = ContributorIssues(user.access_token)
    issues = contributor_issues.get_contributor_issues(repo_fullname, contributor_username)
    return jsonify(issues)



    
