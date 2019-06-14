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
        project = project.name.split("/")
        branch = Branch(chat_id)
        if command == "names":
            branches_data = branch.get_branches_names(
                user.github_user, project[-1])
        elif command == "datecommits":
            branches_data = branch.get_date_last_commit_branches(
                project[-1], user.github_user)
    except HTTPError as http_error:
        return branch.error_message(http_error)
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify(
            branches_data
        ), 200
