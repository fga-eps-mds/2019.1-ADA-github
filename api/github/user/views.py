from flask import jsonify, Blueprint, redirect, request
from flask_cors import CORS
from github.user.utils import UserInfo, send_message,\
                              authenticate_access_token
from github.user.error_messages import NOT_FOUND
from requests.exceptions import HTTPError
from github.data.user import User
import os


github_blueprint = Blueprint("github", __name__)
CORS(github_blueprint)
CLIENT_ID = os.environ.get("GITHUB_OAUTH_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET", "")
GITHUB_REDIRECT_URI = os.getenv("REDIRECT_URI", "")
BOT_NAME = os.environ.get("BOT_NAME", "")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "")


@github_blueprint.route("/user/github/authorize/<chat_id>", methods=["GET"])
def get_access_token(chat_id):
    code = request.args.get('code')
    existing_user = User.objects(chat_id=chat_id).first()
    send_message(ACCESS_TOKEN, chat_id)
    if not existing_user:
        GITHUB_TOKEN = authenticate_access_token(code)
        db_user = User()
        db_user.access_token = GITHUB_TOKEN
        db_user.chat_id = str(chat_id)
        db_user.save()
        user = UserInfo(chat_id)
        user_infos = user.get_own_user_data()
        db_user.github_user = user_infos["github_username"]
        db_user.github_user_id = str(user_infos["github_user_id"])
        db_user.save()
        user.send_button_message(user_infos, chat_id)

    redirect_uri = "https://t.me/{bot_name}".format(bot_name=BOT_NAME)
    return redirect(redirect_uri, code=302)


@github_blueprint.route("/user/repositories/<chat_id>",
                        methods=["GET"])
def get_repositories(chat_id):
    try:
        user = UserInfo(chat_id)
        user_repos = user.get_repositories()
        if len(user_repos) == 0:
            return jsonify(NOT_FOUND), 404
    except HTTPError as http_error:
        return user.error_message(http_error)
    except IndexError:
        return jsonify(NOT_FOUND), 404
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify(
            user_repos
        ), 200


@github_blueprint.route("/user/repo/<chat_id>", methods=["POST"])
def register_repository(chat_id):
    repo_data = request.get_json()
    repo_name = repo_data
    try:
        user = UserInfo(chat_id)
        user.register_repo(repo_name)
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify({
            "status": "OK"
        }), 200


@github_blueprint.route("/user/change_repo/<chat_id>", methods=["GET"])
def change_repository(chat_id):
    user = UserInfo(chat_id)
    user_infos = user.get_own_user_data()
    user.send_button_message(user_infos, chat_id)
