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
                user = req_json["pull_request"]["user"]["login"]
                user_url = req_json["pull_request"]["user"]["html_url"]
                title = req_json["pull_request"]["title"]
                pr_url = req_json["pull_request"]["html_url"]
                message = "❕ **Novo pull request aberto** "\
                          "[{title}]({pr_url})\n"\
                          "por [{user}]({user_url})."\
                          .format(title=title,
                                  pr_url=pr_url,
                                  user=user,
                                  user_url=user_url)
                bot.send_message(chat_id=chat_id, text=message,
                                 parse_mode='Markdown')
            elif "issue" in list(req_json.keys()):
                print("#"*30, file=sys.stderr)
                print("ISSUE ABERTA", file=sys.stderr)
                print("#"*30, file=sys.stderr)
                user = req_json["issue"]["user"]["login"]
                user_url = req_json["issue"]["user"]["html_url"]
                title = req_json["issue"]["title"]
                issue_url = req_json["issue"]["html_url"]
                message = "❇ **Nova issue aberta** "\
                          "[{title}]({issue_url})\n"\
                          "por [{user}]({user_url})."\
                          .format(user=user,
                                  user_url=user_url,
                                  title=title,
                                  issue_url=issue_url)
                bot.send_message(chat_id=chat_id, text=message,
                                 parse_mode='Markdown')
        elif req_json["action"] == "created":
            if "pull_request_review_comment" in list(req_json.keys()):
                print("#"*30, file=sys.stderr)
                print("COMENTÁRIO EM REVIEW DE PR", file=sys.stderr)
                print("#"*30, file=sys.stderr)
            if "issue" in list(req_json.keys()):
                print("#"*30, file=sys.stderr)
                print("NOVO COMENTÁRIO EM ISSUE", file=sys.stderr)
                print("#"*30, file=sys.stderr)
                user = req_json["issue"]["user"]["login"]
                user_url = req_json["issue"]["user"]["html_url"]
                title = req_json["issue"]["title"]
                comment_url = req_json["issue"]["comment"]["html_url"]
                comment_body = req_json["issue"]["comment"]["body"]
                message = "💬 **Novo comentário** "\
                          "[{title}]({comment_url})\n"\
                          "por [{user}]({user_url})\n"\
                          "{comment_body}"\
                          .format(user=user,
                                  user_url=user_url,
                                  title=title,
                                  comment_url=comment_url,
                                  comment_body=comment_body)
                bot.send_message(chat_id=chat_id, text=message,
                                 parse_mode='Markdown')
        elif req_json["action"] == "submitted":
            if "review" in list(req_json.keys()):
                print("#"*30, file=sys.stderr)
                print("REQUEST REALIZADA", file=sys.stderr)
                print("#"*30, file=sys.stderr)
        elif req_json["action"] == "review_requested":
            if "pull_request" in list(req_json.keys()):
                print("#"*30, file=sys.stderr)
                print("REVIEW SOLICITADA", file=sys.stderr)
                print("#"*30, file=sys.stderr)
                user = req_json["pull_request"]["user"]["login"]
                user_url = req_json["pull_request"]["user"]["html_url"]
                title = req_json["pull_request"]["title"]
                pr_url = req_json["pull_request"]["html_url"]
                reviewer = ""
                reviewer += "[" + (req_json["pull_request"]
                                           ["requested_reviewers"]
                                           [0]["login"]) + "]"
                reviewer += "(" + (req_json["pull_request"]
                                           ["requested_reviewers"]
                                           [0]["html_url"]) + ")"
                message = "💻 [{user}]({user_url}) "\
                          "solicitou a revisão de {reviewer} "\
                          "no pull request "\
                          "[{title}]({pr_url})."\
                          .format(title=title,
                                  reviewer=reviewer,
                                  pr_url=pr_url,
                                  user=user,
                                  user_url=user_url)
                bot.send_message(chat_id=chat_id, text=message,
                                 parse_mode='Markdown')
    except KeyError:
        return jsonify({
            "failed": "400"
        }), 400
    else:
        return jsonify({
                "success": "200"
            }), 200
