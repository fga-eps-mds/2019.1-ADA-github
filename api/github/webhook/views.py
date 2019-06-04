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
        post_json = json.loads(request.data)
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


@webhook_blueprint.route("/webhook/delete", methods=["POST"])
def delete_webhook():
    try:
        post_json = json.loads(request.data)
        chat_id = post_json["chat_id"]
        owner = post_json["owner"]
        repo = post_json["repo"]
        webhook = Webhook(chat_id)
        webhook.delete_hook(owner, repo)
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
            if "pull_request" in list(req_json.keys()):  # new pr
                user = req_json["pull_request"]["user"]["login"]
                user_url = req_json["pull_request"]["user"]["html_url"]
                title = req_json["pull_request"]["title"]
                pr_url = req_json["pull_request"]["html_url"]
                repo_name = req_json["repository"]["name"]
                pr_number = req_json["pull_request"]["number"]
                pr_body = req_json["pull_request"]["body"]
                message = "❕ **Novo pull request aberto** em "\
                          "[{repo_name}#{pr_number} "\
                          "{title}]({pr_url})\n"\
                          "por [{user}]({user_url})\n"\
                          "{pr_body}"\
                          .format(repo_name=repo_name,
                                  pr_number=pr_number,
                                  title=title,
                                  pr_url=pr_url,
                                  user=user,
                                  user_url=user_url,
                                  pr_body=pr_body)
                bot.send_message(chat_id=chat_id, text=message,
                                 parse_mode='Markdown',
                                 disable_web_page_preview=True)
            elif "issue" in list(req_json.keys()):  # new issue
                user = req_json["issue"]["user"]["login"]
                user_url = req_json["issue"]["user"]["html_url"]
                title = req_json["issue"]["title"]
                issue_url = req_json["issue"]["html_url"]
                repo_name = req_json["repository"]["name"]
                issue_number = req_json["issue"]["number"]
                message = "❇ **Nova issue aberta** em "\
                          "[{repo_name}#{issue_number} "\
                          "{title}]({issue_url})\n"\
                          "por [{user}]({user_url})."\
                          .format(repo_name=repo_name,
                                  issue_number=issue_number,
                                  user=user,
                                  user_url=user_url,
                                  title=title,
                                  issue_url=issue_url)
                bot.send_message(chat_id=chat_id, text=message,
                                 parse_mode='Markdown',
                                 disable_web_page_preview=True)
        elif req_json["action"] == "created":
            if "pull_request_review_comment" in list(req_json.keys()):
                # new comment on pr review
                pass
            if "issue" in list(req_json.keys()):
                # new issue comment
                user = req_json["issue"]["user"]["login"]
                user_url = req_json["issue"]["user"]["html_url"]
                title = req_json["issue"]["title"]
                comment_url = req_json["comment"]["html_url"]
                comment_body = req_json["comment"]["body"]
                repo_name = req_json["repository"]["name"]
                issue_number = req_json["issue"]["number"]
                message = "💬 **Novo comentário** em "\
                          "[{repo_name}#{issue_number} "\
                          "{title}]({comment_url})\n"\
                          "por [{user}]({user_url})\n"\
                          "{comment_body}"\
                          .format(repo_name=repo_name,
                                  issue_number=issue_number,
                                  user=user,
                                  user_url=user_url,
                                  title=title,
                                  comment_url=comment_url,
                                  comment_body=comment_body)
                bot.send_message(chat_id=chat_id, text=message,
                                 parse_mode='Markdown',
                                 disable_web_page_preview=True)
        elif req_json["action"] == "submitted":
            if "review" in list(req_json.keys()):
                # new reviewed pr
                pass
        elif req_json["action"] == "review_requested":
            if "pull_request" in list(req_json.keys()):
                # new review requested
                user = req_json["pull_request"]["user"]["login"]
                user_url = req_json["pull_request"]["user"]["html_url"]
                title = req_json["pull_request"]["title"]
                pr_url = req_json["pull_request"]["html_url"]
                pr_number = req_json["pull_request"]["number"]
                repo_name = req_json["repository"]["name"]
                reviewer = ""
                reviewer += "[" + (req_json["pull_request"]
                                           ["requested_reviewers"]
                                           [0]["login"]) + "]"
                reviewer += "(" + (req_json["pull_request"]
                                           ["requested_reviewers"]
                                           [0]["html_url"]) + ")"
                message = "📝 [{user}]({user_url}) "\
                          "solicitou a revisão de {reviewer} "\
                          "no pull request "\
                          "[{repo_name}#{pr_number}"\
                          "{title}]({pr_url})."\
                          .format(repo_name=repo_name,
                                  pr_number=pr_number,
                                  title=title,
                                  reviewer=reviewer,
                                  pr_url=pr_url,
                                  user=user,
                                  user_url=user_url)
                bot.send_message(chat_id=chat_id, text=message,
                                 parse_mode='Markdown',
                                 disable_web_page_preview=True)
    except KeyError:
        return jsonify({
            "failed": "400"
        }), 400
    else:
        return jsonify({
                "success": "200"
            }), 200
