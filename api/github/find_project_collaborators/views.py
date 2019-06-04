from flask import jsonify, Blueprint
from requests.exceptions import HTTPError
from flask_cors import CORS
from github.find_project_collaborators.utils import FindProjectCollaborators
from github.data.user import User
from github.find_project_collaborators.error_messages import NOT_FOUND

find_project_collaborators_blueprint = Blueprint("find_project_collaborators",
                                                 __name__)
CORS(find_project_collaborators_blueprint)


@find_project_collaborators_blueprint.route("/api/find_collaborators/" +
                                            "<chat_id>", methods=["GET"])
def find_collaborators(chat_id):
    try:
        user = User.objects(chat_id=chat_id).first()
        project = user.project
        project_name = project.name
        collab = FindProjectCollaborators(chat_id)
        owner_and_repo = collab.get_project(project_name)
        contributors_names = collab.get_collaborators(str(owner_and_repo))

    except HTTPError as http_error:
        return collab.error_message(http_error)
    except AttributeError:
        return jsonify(NOT_FOUND), 404

    else:
        return jsonify(
            {
                "collaborators": contributors_names
            }
        ), 200
