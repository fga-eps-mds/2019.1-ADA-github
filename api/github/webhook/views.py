from flask import jsonify, Blueprint, request
from flask_cors import CORS
from github.branches.error_messages import NOT_FOUND
from requests.exceptions import HTTPError
from github.webhook.webhook_utils import Webhook
import json
import os
from telegram import Bot

webhook_blueprint = Blueprint("webhook", __name__)
CORS(webhook_blueprint)
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "")


@webhook_blueprint.route("/webhook", methods=["POST"])
def set_webhook():
    try:

        post_create_json = json.loads(request.data)
        webhook_create = Webhook(post_create_json["chat_id"])
        create_dict = webhook_create.get_post_info(post_create_json)
        webhook_create.set_webhook(create_dict["owner"],
                                   create_dict["repo"])
    except HTTPError as http_error:
        return webhook_create.error_message(http_error)
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    except KeyError:
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
        return webhook.error_message(http_error)
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify({
            "success": "200"
        }), 200


@webhook_blueprint.route("/github/webhooks/<chat_id>", methods=["POST"])
def webhook_notification(chat_id):
    webhook = Webhook(chat_id)
    req_json = request.json
    try:
        bot = Bot(token=ACCESS_TOKEN)
        user, user_url, title, number, repo_name = \
            webhook.get_message_info(req_json)
        if req_json["action"] == "opened":
            if "pull_request" in list(req_json.keys()):  # new pr
                pr_url = req_json["pull_request"]["html_url"]
                pr_body = req_json["pull_request"]["body"]
                message = "❕ **Novo pull request aberto** em "\
                          "[{repo_name}#{pr_number} "\
                          "{title}]({pr_url})\n"\
                          "por [{user}]({user_url})\n"\
                          "{pr_body}"\
                          .format(repo_name=repo_name,
                                  pr_number=number,
                                  title=title,
                                  pr_url=pr_url,
                                  user=user,
                                  user_url=user_url,
                                  pr_body=pr_body)
                bot.send_message(chat_id=chat_id, text=message,
                                 parse_mode='Markdown',
                                 disable_web_page_preview=True)
            elif "issue" in list(req_json.keys()):  # new issue
                issue_url = req_json["issue"]["html_url"]
                message = "❇ **Nova issue aberta** em "\
                          "[{repo_name}#{issue_number} "\
                          "{title}]({issue_url})\n"\
                          "por [{user}]({user_url})."\
                          .format(repo_name=repo_name,
                                  issue_number=number,
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
                comment_url, comment_body = \
                    webhook.get_body_and_body_url(req_json)
                message = "💬 **Novo comentário** em "\
                          "[{repo_name}#{issue_number} "\
                          "{title}]({comment_url})\n"\
                          "por [{user}]({user_url})\n"\
                          "{comment_body}"\
                          .format(repo_name=repo_name,
                                  issue_number=number,
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
                title = req_json["pull_request"]["title"]
                username = req_json["review"]["user"]["login"]
                user_url = req_json["review"]["user"]["html_url"]
                pull_request_url = req_json["pull_request"]["html_url"]
                review_body = req_json["review"]["body"]
                review_state = ""
                if req_json["review"]["state"] == "approved":
                    review_state = "O seu pull request foi aprovado! ✅\n"
                elif req_json["review"]["state"] == "changes_requested":
                    review_state = "Mudanças foram solicitadas. ❗️\n"

                message = "💬 **Nova revisão no Pull Request**"\
                          " [{title}]({pull_request_url})"\
                          "\nPor: [{username}]({user_url})\n"\
                          .format(title=title,
                                  pull_request_url=pull_request_url,
                                  username=username, user_url=user_url)
                message += review_state
                message += '"{review_body}"'.format(review_body=review_body)
                bot.send_message(chat_id=chat_id,
                                 text=message,
                                 parse_mode='Markdown',
                                 disable_web_page_preview=True)
        elif req_json["action"] == "review_requested":
            if "pull_request" in list(req_json.keys()):
                # new review requested
                pr_url = req_json["pull_request"]["html_url"]
                reviewer = ""
                reviewer += webhook.get_reviewer_login(req_json)
                reviewer += "(" + (req_json["pull_request"]
                                           ["requested_reviewers"]
                                           [0]["html_url"]) + ")"
                message = "📝 [{user}]({user_url}) "\
                          "solicitou a revisão de {reviewer} "\
                          "no pull request "\
                          "[{repo_name}#{pr_number}"\
                          "{title}]({pr_url})."\
                          .format(repo_name=repo_name,
                                  pr_number=number,
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
