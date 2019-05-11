from flask import jsonify, Blueprint, request
from flask_cors import CORS
from github.issue.utils import Issue
import json
from github.issue.error_messages import NOT_FOUND, UNAUTHORIZED
import requests
from requests.exceptions import HTTPError
import os
from github.issue.utils import Issue
from github.data.user import User
from github.data.project import Project

issue_blueprint = Blueprint("issue", __name__)
CORS(issue_blueprint)
GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN", "")


@issue_blueprint.route("/issue/ping", methods=["GET"])
def ping_pong():
    return jsonify({
        "status": "success",
        "message": "pong!"
    }), 200

@issue_blueprint.route("/api/new_issue/<chat_id>",
                       methods=["POST"])
def create_issue(chat_id):
    try:
        response = request.get_json()
        title = response['title']
        body = response['body']

        user = User()
        user = User.objects(chat_id=chat_id).first()
        project = Project()
        project = user.project   
        issue = Issue(GITHUB_API_TOKEN)
        create_issue = issue.create_issue(project.name, title, body)
    except HTTPError as http_error:
        dict_message = json.loads(str(http_error))
        if dict_message["status_code"] == 401:
            return jsonify(UNAUTHORIZED), 401
        else:
            return jsonify(NOT_FOUND), 404
    else:
        return jsonify(
        {
            "title": create_issue["title"],
            "body": create_issue["body"],
            "html_url":create_issue["html_url"]
        }
        ), 200
