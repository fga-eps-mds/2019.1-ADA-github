from flask import jsonify, Blueprint
from flask_cors import CORS
from github.issue.utils import Issue

issue_blueprint = Blueprint("issue", __name__)
CORS(issue_blueprint)

@issue_blueprint.route("/issue/ping", methods=["GET"])
def ping_pong():
    return jsonify({
        "status": "success",
        "message": "pong!"
    }), 200