from flask import jsonify, Blueprint
from flask_cors import CORS
from github.release.utils import Release
from github.data.user import User
from github.release.error_messages import NOT_FOUND
from requests.exceptions import HTTPError

release_blueprint = Blueprint("release", __name__)
CORS(release_blueprint)


@release_blueprint.route("/release/<chat_id>", methods=["GET"])
def get_releases(chat_id):
    try:
        user = User.objects(chat_id=chat_id).first()
        project = user.project
        release = Release(chat_id, user.github_user, project.name)
        release_data = release.get_last_release()
    except HTTPError as http_error:
        user.error_messages(http_error)
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify(
            release_data
            ), 200
