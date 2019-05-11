from flask import jsonify, Blueprint, redirect, request
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
    print(request.args, file=sys.stderr)
    header = {"Accept": "application/json"}

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code
    }

    oauth_user = ("https://github.com/login/oauth/access_token?client_id"
                  "={client_id}&client_secret={client_secret}"
                  "&code={code}".format(
                                  code=code,
                                  client_id=CLIENT_ID,
                                  client_secret=CLIENT_SECRET))
    data = json.dumps(data)
    post = requests.post(url=oauth_user,
                         headers=header)
    post_json = post.json()
    GITHUB_TOKEN = post_json['access_token']
    user_info = UserInfo(GITHUB_TOKEN)
    user_infos = user_info.get_user()

    db_user = User()
    db_user.access_token = GITHUB_TOKEN
    db_user.github_user = user_infos["github_username"]
    db_user.github_user_id = str(user_infos["github_user_id"])

    db_user.save()
    print(GITHUB_TOKEN, file=sys.stderr)

    redirect_uri = "https://t.me/Ada_Git_Bot?start={github_id}".format(
        github_id=db_user.github_user_id)
    return redirect(redirect_uri, code=302)
    # return jsonify({
    #     "message": "success"
    # }), 200


@github_blueprint.route("/user/<github_username>/repositories",
                        methods=["GET"])
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


@github_blueprint.route("/user/<github_id>/<sender_id>", methods=["GET"])
def save_chat_id(github_id, sender_id):
    try:
        user = User.objects(github_user_id=github_id).first()
        user.chat_id = sender_id

        user.save()
    except TypeError:
        print("NOT FOUND", file=sys.stderr)
    else:
        return jsonify({
            "message": "success"
        }), 200
