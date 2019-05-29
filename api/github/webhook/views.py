from flask import jsonify, Blueprint, request
from flask_cors import CORS
from github.branches.error_messages import NOT_FOUND, UNAUTHORIZED
from requests.exceptions import HTTPError
from github.webhook.webhook_utils import Webhook
import json
import sys
import os
import telegram

webhook_blueprint = Blueprint("webhook", __name__)
CORS(webhook_blueprint)
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "")


@webhook_blueprint.route("/webhook", methods=["POST"])
def set_webhook():
    try:
        post_json = request.get_json()
        chat_id = post_json["chat_id"]
        owner = post_json["owner"]
        repo = post_json["repo"]
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

    req_json = request.json
    try:
        bot = telegram.Bot(token=ACCESS_TOKEN)
        if req_json["action"] == "opened":
            if "pull_request" in list(req_json.keys()):
                print("#"*30, file=sys.stderr)
                print("PR ABERTO", file=sys.stderr)
                print("#"*30, file=sys.stderr)
                bot.send_message(chat_id=chat_id, text="NOVO PR")
            elif "issue" in list(req_json.keys()):
                bot.send_message(chat_id=chat_id, text="NOVA ISSUE")
                print("#"*30, file=sys.stderr)
                print("ISSUE ABERTA", file=sys.stderr)
                print("#"*30, file=sys.stderr)
        elif req_json["action"] == "created":
            if "pull_request_review_comment" in list(req_json.keys()):
                print("#"*30, file=sys.stderr)
                print("COMENTÁRIO EM REVIEW DE PR", file=sys.stderr)
                print("#"*30, file=sys.stderr)
            if "issue_comment" in list(req_json.keys()):
                print("#"*30, file=sys.stderr)
                print("NOVO COMENTÁRIO EM ISSUE", file=sys.stderr)
                print("#"*30, file=sys.stderr)
        elif req_json["action"] == "submitted":
            if "review" in list(req_json.keys()):
                print("#"*30, file=sys.stderr)
                print("REQUEST REALIZADA", file=sys.stderr)
                print("#"*30, file=sys.stderr)
        elif req_json["action"] == "review_requested":
            if "pull_request" in list(req_json.keys()):
                bot.send_message(chat_id=chat_id,
                                 text="REVIEW SOLICITADA")
                print("#"*30, file=sys.stderr)
                print("REVIEW SOLICITADA", file=sys.stderr)
                print("#"*30, file=sys.stderr)
    except KeyError:
        return jsonify({
            "failed": "400"
        }), 400
    else:
        return jsonify({
                "success": "200"
            }), 200
