from flask import jsonify, Blueprint
from flask_cors import CORS
from github.pull_request.utils import PullRequest
from github.data.user import User
from github.pull_request.error_messages import NOT_FOUND, UNAUTHORIZED
from requests.exceptions import HTTPError
import json


pull_request_blueprint = Blueprint("pull_request", __name__)
CORS(pull_request_blueprint)


@pull_request_blueprint.route("/pullrequest/ping", methods=["GET"])
def ping_pong():
    return jsonify({
        "status": "success",
        "message": "pong!"
    }), 200


@pull_request_blueprint.route("/pullrequest/<chat_id>", methods=["GET"])
def get_pull_request(chat_id):
    try:
        user = User.objects(chat_id=chat_id).first()
        project = user.project
        pull_request = PullRequest(user.access_token)
        pull_request_data = pull_request.get_pull_requests(user.github_user,
                                                           project.name)
    except HTTPError as http_error:
        dict_message = json.loads(str(http_error))
        if dict_message["status_code"] == 401:
            return jsonify(UNAUTHORIZED), 401
        else:
            return jsonify(NOT_FOUND), 404
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify(
            pull_request_data
            ), 200
