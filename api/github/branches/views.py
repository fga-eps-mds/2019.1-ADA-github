from flask import jsonify, Blueprint
from flask_cors import CORS
from github.branches.utils import Branch
from github.data.user import User


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
    user = User.objects(chat_id=chat_id).first()
    project = user.project
    branch = Branch(user.access_token)
    branches_names = branch.get_branches_names(project.name, user.github_user)
    return jsonify(
        branches_names
        ), 200


@branches_blueprint.route("/branches/datecommits/<chat_id>", methods=["GET"])
def get_commits_dates(chat_id):
    user = User.objects(chat_id=chat_id).first()
    project = user.project
    branch = Branch(user.access_token)
    commits_date = branch.get_date_last_commit_branches(project.name,
                                                        user.github_user)
    return jsonify(
        commits_date
        ), 200
