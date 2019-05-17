from flask import jsonify, Blueprint, redirect, url_for, request
from flask_cors import CORS
from github.user.utils import UserInfo
from github.user.error_messages import NOT_FOUND, UNAUTHORIZED
from requests.exceptions import HTTPError
from github.data.user import User
import telegram
import requests
import sys
import json
import os

github_blueprint = Blueprint("github", __name__)
CLIENT_ID = os.environ.get("GITHUB_OAUTH_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET", "")
BOT_NAME = os.environ.get("BOT_NAME", "")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "")
CORS(github_blueprint)

@github_blueprint.route("/user/ping", methods=["GET"])
def ping_pong():
    return jsonify({
        "status": "success",
        "message": "pong!"
    }), 200


@github_blueprint.route("/user/github/authorize/<chat_id>", methods=["GET"])
def get_access_token(chat_id):
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
    post_json = post.json()
    GITHUB_TOKEN = post_json['access_token']
    print(GITHUB_TOKEN, file=sys.stderr)
    user = UserInfo(GITHUB_TOKEN)
    user_infos = user.get_user()


    db_user = User()
    db_user.access_token = GITHUB_TOKEN
    db_user.github_user = user_infos["github_username"]
    db_user.github_user_id = str(user_infos["github_user_id"])
    db_user.chat_id = str(chat_id)
    db_user.save()
    user.send_message(ACCESS_TOKEN, chat_id)
    redirect_uri = "https://t.me/{bot_name}".format(bot_name=BOT_NAME)
    bot = telegram.Bot(token=ACCESS_TOKEN)
    repo_names = user.select_repos_by_buttons(user)
    reply_markup = telegram.InlineKeyboardMarkup(repo_names)
    bot.send_message(chat_id=chat_id,
                         text="Encontrei esses repositórios na sua "
                         "conta. Qual você quer que eu "
                         "monitore? Clica nele!",
                         reply_markup=reply_markup)
    return redirect(redirect_uri, code=302)

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

@github_blueprint.route("/user/<chat_id>", methods=["GET"])
def get_github_login(chat_id):
    try:
        db_user = User.objects(chat_id=chat_id).first()
        username = db_user.github_user
        print(username, file=sys.stderr)
    except HTTPError as http_error:
        dict_message = json.loads(str(http_error))
        if dict_message["status_code"] == 401:
            return jsonify(UNAUTHORIZED), 401
        else:
            return jsonify(NOT_FOUND), 404
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify({
            "username": username
        }), 200

@github_blueprint.route("/user/repo", methods=["POST"])
def register_repository():
    repo_data = request.get_json()
    repo_name = repo_data
    try:
        db_user = User()
        user_repositories = UserInfo(db_user.access_token)
        user_repositories.register_repo(repo_name)
    except HTTPError as http_error:
        dict_message = json.loads(str(http_error))
        return jsonify(dict_message), 400
    except AttributeError as attribute_error:
        dict_message = json.loads(str(attribute_error))
        return jsonify(dict_message), 400
    else:
        return jsonify({
            "status": "OK"
        }), 200
