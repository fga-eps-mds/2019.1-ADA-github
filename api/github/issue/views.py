from flask import jsonify, Blueprint, request
from flask_cors import CORS
from github.issue.utils import Issue
from github.issue.error_messages import NOT_FOUND
from requests.exceptions import HTTPError
from github.data.user import User
from github.data.project import Project

issue_blueprint = Blueprint("issue", __name__)
CORS(issue_blueprint)


@issue_blueprint.route("/api/new_issue/<chat_id>", methods=["POST"])
def create_issue(chat_id):
    try:
        response = request.get_json()
        title = response['title']
        body = response['body']

        user = User.objects(chat_id=chat_id).first()
        project = Project()
        project = user.project
        project = project.name.split("/")
        issue = Issue(chat_id)
        create_issue = issue.create_issue(project[-1], user.github_user,
                                          title, body)
    except HTTPError as http_error:
        return issue.error_message(http_error)
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify({
                "title": create_issue["title"],
                "body": create_issue["body"],
                "html_url": create_issue["html_url"]
            }
        ), 200
