# api/github/__init__.py

from github.data.user import User
from github.data.project import Project
from github.utils.github_utils import GitHubUtils
import requests
import json
import telegram
import os

CLIENT_ID = os.getenv("GITHUB_OAUTH_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("GITHUB_OAUTH_CLIENT_SECRET", "")
GITHUB_REDIRECT_URI = os.getenv("REDIRECT_URI", "")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "")


class UserInfo(GitHubUtils):
    def __init__(self, chat_id):
        super().__init__(chat_id)
        self.headers = {
            "Content-Type": "application/json"
        }

    def get_own_user_data(self):
        url = self.GITHUB_API_URL + "user?access_token="\
                                    "{access_token}".format(
                                     access_token=self.GITHUB_API_TOKEN)
        requested_user = self.get_request(url)
        github_data = {"github_username": requested_user["login"],
                       "github_user_id": requested_user["id"]}
        return github_data

    def get_repositories(self):
        requested_username = self.get_own_user_data()
        username = requested_username["github_username"]
        url = self.GITHUB_API_URL + "users/{login}/repos?access_token="\
                                    "{access_token}".format(
                                     login=username, access_token=self
                                     .GITHUB_API_TOKEN)
        requested_repositories = self.get_request(url)
        repositories = {"repositories": []}
        for i, item in enumerate(requested_repositories):
            repository_data = {"name": 0}
            self.update_repositories_data(repository_data, repositories,
                                          requested_repositories, i)
        return repositories

    def update_repositories_data(self, repository_data,
                                 repositories, resp, count):
        repository_data["name"] = resp[count]['name']
        repositories["repositories"].append(repository_data)

    def select_repos_by_buttons(self, user):
        received_repositories = user.get_repositories()
        buttons = []
        for repositorio in received_repositories["repositories"]:
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


def authenticate_access_token(code):
    header = {"Accept": "application/json"}
    redirect_uri = GITHUB_REDIRECT_URI
    data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "redirect_uri": redirect_uri
    }
    url = ("https://github.com/login/oauth/access_token?client_id"
           "={client_id}&client_secret={client_secret}"
           "&code={code}".format(
                                 code=code,
                                 client_id=CLIENT_ID,
                                 client_secret=CLIENT_SECRET))
    data = json.dumps(data)
    post = requests.post(url=url,
                         headers=header,
                         data=data)
    post_json = post.json()
    GITHUB_TOKEN = post_json['access_token']
    return GITHUB_TOKEN


def send_message(token, chat_id):
    access_token = os.environ.get("ACCESS_TOKEN", "")
    bot = telegram.Bot(token=access_token)
    bot.send_message(chat_id=chat_id,
                     text="Você foi cadastrado com sucesso "
                          "no GitHub")
