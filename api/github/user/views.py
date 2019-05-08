from flask import jsonify, Blueprint, redirect, url_for, request
from flask_cors import CORS
from github.user.utils import User
from github.user.error_messages import NOT_FOUND, UNAUTHORIZED
from requests.exceptions import HTTPError
import requests
import sys
import json
import os

github_blueprint = Blueprint("github", __name__)
CLIENT_ID = os.environ.get("GITHUB_OAUTH_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET", "")
CORS(github_blueprint)

@github_blueprint.route("/user/ping", methods=["GET"])
def ping_pong():
    return jsonify({
        "status": "success",
        "message": "pong!"
    }), 200


@github_blueprint.route("/user/signin/callback", methods=["GET"])
def index():
    code = request.args.get('code')
    header = {"Accept": "application/json"}

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code
    }
    scope = "admin:repo_hook,repo"
    oauth_user = "https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}".format(
        code=code, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    data = json.dumps(data)
    post = requests.post(url=oauth_user,
                         headers=header)
    post_str = post.json()
    GITHUB_TOKEN = post_str['access_token']
    try:
        user = User(GITHUB_TOKEN)
        username = user.get_user()
        requested_repos = user.get_repos()
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
            username,
            requested_repos
        ), 200

