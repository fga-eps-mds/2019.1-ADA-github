from flask import jsonify, Blueprint, request
from flask_cors import CORS
from github.branches.error_messages import NOT_FOUND, UNAUTHORIZED
from requests.exceptions import HTTPError
from github.webhook.webhook_utils import Webhook
import json
import sys

webhook_blueprint = Blueprint("webhook", __name__)
CORS(webhook_blueprint)


@webhook_blueprint.route("/webhook/<chat_id>/<owner>/"
                         "<repo>", methods=["GET"])
def set_webhook(chat_id, owner, repo):
    try:
        webhook = Webhook(chat_id)
        webhook.set_webhook(owner, repo)
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
            "success": "200"
        }), 200


@webhook_blueprint.route("/github/webhooks/<chat_id>", methods=["POST"])
def webhook_notification(chat_id):
    print("#"*30, file=sys.stderr)
    print(request.data, file=sys.stderr)
    print("#"*30, file=sys.stderr)
    return jsonify({
            "success": "200"
        }), 200
