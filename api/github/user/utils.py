# api/github/__init__.py

import requests
from github.data.user import User
from github.data.project import Project
import json
import telegram
import os


class UserInfo():
    def __init__(self, GITHUB_TOKEN):
        self.GITHUB_TOKEN = GITHUB_TOKEN

    def get_user(self):
        headers = {
            "Content-Type": "applications/json",
            "Authorization": "Bearer " + self.GITHUB_TOKEN
        }
        response = requests.get('https://api.github.com/user', headers=headers)
        requested_user = response.json()
        github_data = {"github_username": requested_user["login"],
                       "github_user_id": requested_user["id"]}
        return github_data

    def get_repos(self):
        headers = {
            "Content-Type": "applications/json",
            "Authorization": "Bearer " + self.GITHUB_TOKEN
        }
        github_username = self.get_user()
        login = github_username["github_username"]
        response = requests.get('https://api.github.com/users/{login}/repos'.
                                format(login=login), headers=headers)
        repository = response.json()
        requested_repositories = {"repositories": []}
        for i, item in enumerate(repository):
            repository_data = {"name": 0}
            repository_data["name"] = repository[i]['name']
            requested_repositories["repositories"].append(repository_data)
        print(requested_repositories["repositories"])
        return requested_repositories

    def send_message(self, token, chat_id):
        github_username = self.get_user()
        login = github_username["github_username"]
        access_token = os.environ.get("ACCESS_TOKEN", "")
        bot = telegram.Bot(token=access_token)
        bot.send_message(chat_id=chat_id,
                         text="Você foi cadastrado com sucesso"
                              "no GitHub, {user}".format(user=login))

    def select_repos_by_buttons(self, user):
        received_repos = user.get_repos()
        buttons = []
        for repositorio in received_repos["repositories"]:
            buttons.append(telegram.InlineKeyboardButton(
                    text=repositorio["name"],
                    callback_data="meu repositorio do github é " +
                                  repositorio["name"]))
        repo_names = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
        return repo_names

    def register_repo(self, repo_json):
        project_name = repo_json["repository_name"]
        chat_id = repo_json["chat_id"]

        user = User.objects(chat_id=chat_id).first()
        try:
            project = Project()
            project.save_repository_infos(user, project_name)
            user.save_github_repo_data(project)
        except AttributeError:
            dict_error = {"message":
                          "Tive um erro tentando cadastrar seu repositório. "
                          "Mais tarde você tenta. Ok?"}
            raise AttributeError(json.dumps(dict_error))
