from flask import jsonify, Blueprint
from flask_cors import CORS
from github.contributor_issues.utils import ContributorIssues
import json
from github.issue.error_messages import NOT_FOUND, UNAUTHORIZED
from requests.exceptions import HTTPError
from github.data.user import User
import sys

contributor_issues_blueprint = Blueprint("contributor_issues", __name__)
CORS(contributor_issues_blueprint)


@contributor_issues_blueprint.route("/api/get_contributor_issues/<chat_id>/"
                                    "<contributor_username>", methods=["GET"])
def get_contributor_issues(chat_id, contributor_username):
    try:
        print("###"*60 + "\n" + chat_id + "###"*60 + "\n", file=sys.stderr)
        user = User.objects(chat_id=chat_id).first()
        project = user.project
        contributor_issues = ContributorIssues(user.access_token)
        issues = contributor_issues.\
            get_contributor_issues(project.name, contributor_username)
    except HTTPError as http_error:
        dict_message = json.loads(str(http_error))
        if dict_message["status_code"] == 401:
            return jsonify(UNAUTHORIZED), 401
        else:
            return jsonify(NOT_FOUND), 404
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify(issues), 200
