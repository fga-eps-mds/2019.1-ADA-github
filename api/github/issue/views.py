from flask import jsonify, Blueprint, request
from flask_cors import CORS
from github.issue.utils import Issue
import json
from github.issue.error_messages import NOT_FOUND, UNAUTHORIZED
from requests.exceptions import HTTPError
import os
from github.data.user import User
from github.data.project import Project
import sys

issue_blueprint = Blueprint("issue", __name__)
CORS(issue_blueprint)

@issue_blueprint.route("/issue/ping", methods=["GET"])
def ping_pong():
    return jsonify({
        "status": "success",
        "message": "pong!"
    }), 200

@issue_blueprint.route("/api/new_issue/<chat_id>", methods=["POST"])
def create_issue(chat_id):
    try:
        response = request.get_json()
        title = response['title']
        body = response['body']

        user = User()
        user = User.objects(chat_id=chat_id).first()
        project = Project()
        project = user.project
        issue = Issue(user.access_token)
        print(issue, file=sys.stderr) # Verificar o que está saindo aqui
        create_issue = issue.create_issue(project.name, user.github_user,
                                          title, body)
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
         {
            "title": create_issue["title"],
            "body": create_issue["body"],
            "html_url": create_issue["html_url"]
         }
        ), 200
