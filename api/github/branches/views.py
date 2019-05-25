from flask import jsonify, Blueprint
from flask_cors import CORS
from github.branches.utils import Branch
from github.data.user import User
from github.branches.error_messages import NOT_FOUND, UNAUTHORIZED
from requests.exceptions import HTTPError
import json


branches_blueprint = Blueprint("branches", __name__)
CORS(branches_blueprint)


@branches_blueprint.route("/branches/ping", methods=["GET"])
def ping_pong():
    return jsonify({
        "status": "success",
        "message": "pong!"
    }), 200


@branches_blueprint.route("/branches/names/<chat_id>", methods=["GET"])
def get_branches(chat_id):
    try:
        user = User.objects(chat_id=chat_id).first()
        project = user.project
        branch = Branch(user.access_token)
        branches_names = branch.get_branches_names(
                         project.name, user.github_user)
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
            branches_names
            ), 200


@branches_blueprint.route("/branches/datecommits/<chat_id>", methods=["GET"])
def get_commits_dates(chat_id):
    try:
        user = User.objects(chat_id=chat_id).first()
        project = user.project
        branch = Branch(user.access_token)
        commits_date = branch.get_date_last_commit_branches(project.name,
                                                            user.github_user)

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
            commits_date
            ), 200
