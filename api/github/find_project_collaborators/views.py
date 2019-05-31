from flask import jsonify, Blueprint, request
import json
from requests.exceptions import HTTPError
from flask_cors import CORS
from github.find_project_collaborators.utils import FindProjectCollaborators
from github.user.utils import User
from github.data.user import User
from github.data.project import Project
from github.find_project_collaborators.error_messages import NOT_FOUND,\
                                                             UNAUTHORIZED
import sys


find_project_collaborators_blueprint = Blueprint("find_project_collaborators",
                                                      __name__)
CORS(find_project_collaborators_blueprint)

@find_project_collaborators_blueprint.route("/api/find_collaborators/<chat_id>",
                                                 methods=["GET"])
def find_collaborators(chat_id):
    try:

        # achar o usuario e o projeto dele
        user = User()
        user = User.objects(chat_id=chat_id).first()
        project = Project()
        project = user.project
        project_name = project.name
        # passar isso pra classe principal da utils
        collab = FindProjectCollaborators(user.access_token)
        # encontrar as info do projeto: chamar a get_project()
        owner_and_repo = collab.get_project(project_name)
        # econtrar os colaboradores do projeto
        contributors_names = collab.get_collaborators(str(owner_and_repo))

    except HTTPError as http_error:
        dict_message = json.loads(str(http_error))
        if dict_message["status_code"] == 401:
            return jsonify(UNAUTHORIZED), 401
        else:
            return jsonify(NOT_FOUND), 404

    except AttributeError:
        return jsonify(NOT_FOUND), 404

    else:
        return jsonify(contributors_names), 200
