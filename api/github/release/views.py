from flask import jsonify, Blueprint
from flask_cors import CORS
from github.release.utils import Release
from github.data.user import User
from github.release.error_messages import NOT_FOUND, UNAUTHORIZED
from requests.exceptions import HTTPError
import json

release_blueprint = Blueprint("release", __name__)
CORS(release_blueprint)


@release_blueprint.route("/release/ping", methods=["GET"])
def ping_pong():
    return jsonify({
        "status": "success",
        "message": "pong!"
    }), 200


@release_blueprint.route("/release/<chat_id>", methods=["GET"])
def get_releases(chat_id):
    try:
        user = User.objects(chat_id=chat_id).first()
        project = user.project
        release = Release(user.access_token)
        release_data = release.get_last_release(user.github_user,
                                                project.name)
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
            release_data
            ), 200
