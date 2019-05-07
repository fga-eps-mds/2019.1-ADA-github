from flask import jsonify, Blueprint, redirect, url_for, request
from flask_cors import CORS
from github.user.utils import User
import requests
import sys
import json
import os

github_blueprint = Blueprint("github", __name__)
CLIENT_ID = os.environ.get("GITHUB_OAUTH_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET", "")
CORS(github_blueprint)

@github_blueprint.route("/user/ping", methods=["GET"])
def ping_pong():
    return jsonify({
        "status": "success",
        "message": "pong!"
    }), 200

@github_blueprint.route("/user/signin/callback", methods=["GET"])
def index():
    code = request.args.get('code')
    header = {"Content-Type": "application/json"}
    
    data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code
            }
    scope = "admin:repo_hook,repo"
    a = "https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}".format(
        code=code, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    data = json.dumps(data)
    post = requests.post(url=a,
                         headers=header)
    # return token
    post_str = str(post.content)
    # post_str = post_str.split("=")[1]
    # access_token = post_str.replace("&scope","")
    print(post_str, file=sys.stderr)
    #save to db

    return jsonify({"message": "success"})
    # return access_token
