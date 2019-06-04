from flask import jsonify, Blueprint
from flask_cors import CORS
from github.branches.utils import Branch
from github.data.user import User
from github.branches.error_messages import NOT_FOUND
from requests.exceptions import HTTPError


branches_blueprint = Blueprint("branches", __name__)
CORS(branches_blueprint)


@branches_blueprint.route("/branches/<command>/<chat_id>", methods=["GET"])
def get_branches(command, chat_id):
    try:
        user = User.objects(chat_id=chat_id).first()
        project = user.project
        branch = Branch(chat_id)
        if command == "names":
            branches_data = branch.get_branches_names(
                user.github_user, project.name)
        elif command == "datecommits":
            branches_data = branch.get_date_last_commit_branches(
                project.name, user.github_user)
    except HTTPError as http_error:
        return branch.error_message(http_error)
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify(
            branches_data
        ), 200


# @branches_blueprint.route("/branches/names/<chat_id>", methods=["GET"])
# def get_branches(chat_id):
#     try:
#         user = User.objects(chat_id=chat_id).first()
#         project_branches = user.project
#         branch = Branch(chat_id)
#         branches_names = branch.get_branches_names(
#                             user.github_user, project_branches.name)
#     except HTTPError as http_error:
#         user.error_message(http_error)
#     except AttributeError:
#         return jsonify(NOT_FOUND), 404
#     else:
#         return jsonify(
#             branches_names
#             ), 200


# @branches_blueprint.route("/branches/datecommits/<chat_id>", methods=["GET"])
# def get_commits_dates(chat_id):
#     try:
#         user = User.objects(chat_id=chat_id).first()
#         project = user.project
#         branch = Branch(chat_id)
#         commits_date = branch.get_date_last_commit_branches(project.name,
#                                                             user.github_user)
#     except HTTPError as http_error:
#         user.error_message(http_error)
#     except AttributeError:
#         return jsonify(NOT_FOUND), 404
#     else:
#         return jsonify(
#             commits_date
#             ), 200
