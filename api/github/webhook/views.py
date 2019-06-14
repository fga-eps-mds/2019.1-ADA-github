from flask import jsonify, Blueprint, request
from flask_cors import CORS
from github.branches.error_messages import NOT_FOUND
from requests.exceptions import HTTPError
from github.webhook.webhook_utils import Webhook
import json
import os
from telegram import Bot
import telegram

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
        dict_message = webhook.get_message_info(req_json)
        if req_json["action"] == "opened":
            if "pull_request" in list(req_json.keys()):  # new pr
                message = "❕ *Novo pull request aberto* em "\
                          "[{repo_name}#{pr_number} "\
                          "{title}]({pr_url})\n"\
                          "por [{user}]({user_url})\n\n"\
                          "{pr_body}"\
                          .format(repo_name=dict_message["repo_name"],
                                  pr_number=dict_message["number"],
                                  title=dict_message["title"],
                                  pr_url=dict_message["url"],
                                  user=dict_message["user"],
                                  user_url=dict_message["user_url"],
                                  pr_body=dict_message["body"])
                bot.send_message(chat_id=chat_id, text=message,
                                 parse_mode=telegram.ParseMode.MARKDOWN,
                                 disable_web_page_preview=True)
            elif "issue" in list(req_json.keys()):  # new issue
                message = "❇ *Nova issue aberta* em "\
                          "[{repo_name}#{issue_number} "\
                          "{title}]({issue_url})\n"\
                          "por [{user}]({user_url}).\n\n"\
                          "_Caso você queira comentar "\
                          "essa issue, é só você escrever: 'Comentar "\
                          "#{issue_number}: e o comentário aqui'_"\
                          .format(repo_name=dict_message["repo_name"],
                                  issue_number=dict_message["number"],
                                  user=dict_message["user"],
                                  user_url=dict_message["user_url"],
                                  title=dict_message["title"],
                                  issue_url=dict_message["url"])
                bot.send_message(chat_id=chat_id, text=message,
                                 parse_mode=telegram.ParseMode.MARKDOWN,
                                 disable_web_page_preview=True)
        elif req_json["action"] == "created":
            if "pull_request_review_comment" in list(req_json.keys()):
                # new comment on pr review
                pass
            if "issue" in list(req_json.keys()):
                # new issue comment
                comment_url, comment_body = \
                    webhook.get_body_and_body_url(req_json)
                message = "💬 *Novo comentário* em "\
                          "[{repo_name}#{issue_number} "\
                          "{title}]({comment_url})\n"\
                          "por [{user}]({user_url})\n"\
                          "\n{comment_body}\n\n_Caso você queira comentar "\
                          "essa issue, é só você escrever: 'Comentar "\
                          "#{issue_number}: e o comentário aqui'_"\
                          .format(repo_name=dict_message["repo_name"],
                                  issue_number=dict_message["number"],
                                  user=dict_message["user"],
                                  user_url=dict_message["user_url"],
                                  title=dict_message["title"],
                                  comment_url=comment_url,
                                  comment_body=comment_body)
                bot.send_message(chat_id=chat_id, text=message,
                                 parse_mode=telegram.ParseMode.MARKDOWN,
                                 disable_web_page_preview=True)
        elif req_json["action"] == "submitted":
            if "review" in list(req_json.keys()):
                # new reviewed pr
                pull_request_name = "[{title}]({url})".format(
                                    title=dict_message["title"],
                                    url=dict_message["url"])
                if req_json["review"]["state"] == "approved":
                    review_state = "✅ Pull request " + pull_request_name +\
                                   " aprovado"
                elif req_json["review"]["state"] == "changes_requested":
                    review_state = " ❗️Mudanças solicitadas no pull request" +\
                                    " " + pull_request_name
                else:
                    review_state = "💬 Pull request " + pull_request_name +\
                                   "revisado"
                message = review_state + " por [@{username}]({user_url})\n\n"\
                                         .format(username=dict_message["user"],
                                                 user_url=dict_message
                                                 ["user_url"])
                message += '{review_body}'.format(review_body=dict_message
                                                  ["body"])
                bot.send_message(chat_id=chat_id,
                                 text=message,
                                 parse_mode='Markdown',
                                 disable_web_page_preview=True)
        elif req_json["action"] == "review_requested":
            if "pull_request" in list(req_json.keys()):
                # new review requested
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
                          .format(repo_name=dict_message["repo_name"],
                                  pr_number=dict_message["number"],
                                  title=dict_message["title"],
                                  reviewer=reviewer,
                                  pr_url=dict_message["url"],
                                  user=dict_message["user"],
                                  user_url=dict_message["user_url"])
                bot.send_message(chat_id=chat_id, text=message,
                                 parse_mode=telegram.ParseMode.MARKDOWN,
                                 disable_web_page_preview=True)
    except KeyError:
        return jsonify({
            "failed": "400"
        }), 400
    else:
        return jsonify({
                "success": "200"
            }), 200
