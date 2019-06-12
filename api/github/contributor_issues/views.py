from flask import jsonify, Blueprint
from flask_cors import CORS
from github.contributor_issues.utils import ContributorIssues
from github.find_project_collaborators.utils import FindProjectCollaborators
from github.issue.error_messages import NOT_FOUND
from requests.exceptions import HTTPError
from github.data.user import User

contributor_issues_blueprint = Blueprint("contributor_issues", __name__)
CORS(contributor_issues_blueprint)


@contributor_issues_blueprint.route("/api/get_contributor_issues/<chat_id>/"
                                    "<contributor_username>", methods=["GET"])
def get_contributor_issues(chat_id, contributor_username):
    try:
        user = User.objects(chat_id=chat_id).first()
        project = user.project
        project_collaborator = FindProjectCollaborators(chat_id)
        full_name = project_collaborator.get_project(project.name)
        contributor_issues = ContributorIssues(chat_id)
        issues = contributor_issues.\
            get_contributor_issues(full_name, contributor_username)
    except HTTPError as http_error:
        return contributor_issues.error_message(http_error)
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify(issues), 200
