from flask import jsonify, Blueprint, redirect, request
from flask_cors import CORS
from github.branches.utils import Branch
from github.user.error_messages import NOT_FOUND, UNAUTHORIZED
from requests.exceptions import HTTPError
from github.data.user import User
import sys

branches_blueprint = Blueprint("branches", __name__)
CORS(branches_blueprint)


@branches_blueprint.route("/branches/ping", methods=["GET"])
def ping_pong():
    return jsonify({
        "status": "success",
        "message": "pong!"
    }), 200


@branches_blueprint.route("/branches/<chat_id>", methods=["GET"])
def get_branches(chat_id):
    user = User.objects(chat_id=chat_id).first()
    project = user.project
    branch = Branch(user.access_token)
    branches_names = branch.get_branches_names(project.name, user.github_user)
    return jsonify(
        branches_names
        ), 200
