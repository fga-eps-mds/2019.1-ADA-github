from flask import jsonify, Blueprint
from flask_cors import CORS
from github.pull_request.utils import PullRequest
from github.data.user import User
from github.pull_request.error_messages import NOT_FOUND
from requests.exceptions import HTTPError


pull_request_blueprint = Blueprint("pull_request", __name__)
CORS(pull_request_blueprint)


@pull_request_blueprint.route("/pullrequest/<chat_id>", methods=["GET"])
def get_pull_request(chat_id):
    try:
        user = User.objects(chat_id=chat_id).first()
        project = user.project
        pull_request = PullRequest(chat_id)
        pull_request_data = pull_request.get_pull_requests(user.github_user,
                                                           project.name)
    except HTTPError as http_error:
        user.error_message(http_error)
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify(
            pull_request_data
            ), 200
