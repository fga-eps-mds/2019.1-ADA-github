# api/github/__init__.py

from requests.exceptions import HTTPError
from flask import jsonify
from github.data.user import User
from github.utils.error_messages import UNAUTHORIZED,\
    NOT_FOUND
import json
import requests
import re


class GitHubUtils:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.GITHUB_API_TOKEN = self.get_access_token(self.chat_id)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(self.GITHUB_API_TOKEN)
        }
        self.GITHUB_API_URL = "https://api.github.com/"

    def get_access_token(self, chat_id):
        user = User.objects(chat_id=chat_id).first()
        return user.access_token

    def error_message(self, http_error):
        dict_message = json.loads(str(http_error))
        if dict_message["status_code"] == 401:
            return jsonify(UNAUTHORIZED), 401
        else:
            return jsonify(NOT_FOUND), 404

    def request_url(self, url, request_type, data=None):
        try:
            if request_type == "get":
                response = requests.get(url, headers=self.headers)
            elif request_type == "post":
                response = requests.post(url, headers=self.headers,
                                         data=json.dumps(data))
            else:
                raise AttributeError(self.exception_json(404))
            response.raise_for_status()
        except HTTPError as http_error:
            raise HTTPError(self.exception_json(http_error.
                                                response.
                                                status_code))
        else:
            resp_json = response.json()
            return resp_json

    def exception_json(self, message):
        error_dict = {"status_code": message}
        return json.dumps(error_dict)

    def get_class_type(self, object):
        raw_class_name = str(type(object)).split('.')[-1]
        class_name = re.sub('[^a-zA-Z]+', '', raw_class_name)
        return class_name

    def project_owner_project_name(self, project_owner, project_name, name):
        url = "repos/{project_owner}/{project_name}/"\
              "{name}".format(
               project_owner=project_owner,
               project_name=project_name, name=name)
        return url
