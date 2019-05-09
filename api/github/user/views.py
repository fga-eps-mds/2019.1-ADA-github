from flask import jsonify, Blueprint, redirect, url_for, request
from flask_cors import CORS
from github.user.utils import UserInfo
from github.user.error_messages import NOT_FOUND, UNAUTHORIZED
from requests.exceptions import HTTPError
from github.data.user import User
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


@github_blueprint.route("/user/callback", methods=["GET"])
def get_access_token():
    code = request.args.get('code')
    print("$"*40, file=sys.stderr)
    print(code, file=sys.stderr)
    print("$"*40, file=sys.stderr)
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
    post_json = post.json()
    GITHUB_TOKEN = post_json['access_token']
    user_info = UserInfo(GITHUB_TOKEN)
    user_infos = user_info.get_user()

    db_user = User()
    db_user.access_token = GITHUB_TOKEN
    db_user.github_user = user_infos
    db_user.save()
    print(GITHUB_TOKEN, file=sys.stderr)

    return redirect("https://t.me/Ada_a_bot", code=302)
    # return jsonify({
    #     "message": "success"
    # }), 200


@github_blueprint.route("/user/<github_username>/repositories", methods=["GET"])
def get_repositories(github_username):
    try:
        db_user = User.objects(github_user=github_username).first()
        user_repositories = UserInfo(db_user.access_token)

        requested_repos = user_repositories.get_repos()
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
            requested_repos
        ), 200
