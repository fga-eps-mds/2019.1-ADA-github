from flask import jsonify, Blueprint, request
from flask_cors import CORS
from github.pull_request.utils import PullRequest
from github.data.user import User
from github.pull_request.error_messages import NOT_FOUND
from requests.exceptions import HTTPError
from github.data.project import Project


pull_request_blueprint = Blueprint("pull_request", __name__)
CORS(pull_request_blueprint)


@pull_request_blueprint.route("/pullrequest/<chat_id>", methods=["GET"])
def get_pull_request(chat_id):

    try:
        user = User.objects(chat_id=chat_id).first()
        project_pr = user.project
        project_pr = project_pr.name.split("/")
        pull_request = PullRequest(chat_id)
        pull_request_data = pull_request.get_pull_requests(user.github_user,
                                                           project_pr[-1])
    except HTTPError as http_error:
        return pull_request.error_message(http_error)
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify(
            pull_request_data
            ), 200


@pull_request_blueprint.route("/api/new_pr/<chat_id>", methods=["POST"])
def create_pull_request(chat_id):

    try:
        response = request.get_json()
        title = response["title"]
        body = response["body"]
        head = response["head"]
        base = response["base"]

        user = User.objects(chat_id=chat_id).first()
        project = Project()
        project = user.project
        project = project.name.split("/")
        pull_request = PullRequest(chat_id)
        create_pr = pull_request.create_pull_request(project[-1],
                                                     title, body,
                                                     user.github_user,
                                                     head, base)
    except HTTPError as http_error:
        return pull_request.error_message(http_error)
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify({
            "title": create_pr["title"],
            "body": create_pr["body"],
            "head": create_pr["head"],
            "base": create_pr["base"]
        }), 200
