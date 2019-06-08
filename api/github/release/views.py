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
        project_release = user.project
        project_release = project_release.name.split("/")
        release = Release(chat_id, user.github_user, project_release[-1])
        release_data = release.get_last_release()
    except HTTPError as http_error:
        return release.error_message(http_error)
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify(
            release_data
            ), 200
