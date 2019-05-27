from flask import jsonify, Blueprint, request
from flask_cors import CORS
from github.find_project_collaborators.utils import FindProjectCollaborators


find_project_collaborators_blueprint = Blueprint("find_project_collaborators",
                                                  __name__)
CORS(find_project_collaborators_blueprint)

@find_project_collaborators_blueprint.route("/api/find_collaborators/<chat_id>",
                                             methods=["GET"])
