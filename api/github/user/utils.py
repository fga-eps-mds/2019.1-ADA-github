# api/github/__init__.py
from github.webhook.webhook_utils import Webhook
from github.data.user import User
from github.data.project import Project
from github.utils.github_utils import GitHubUtils
import json
import telegram
import os
from requests import post

CLIENT_ID = os.getenv("GITHUB_OAUTH_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("GITHUB_OAUTH_CLIENT_SECRET", "")
GITHUB_REDIRECT_URI = os.getenv("REDIRECT_URI", "")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "")


class UserInfo(GitHubUtils):
    def __init__(self, chat_id):
        super().__init__(chat_id)

    def get_own_user_data(self):
        url = self.GITHUB_API_URL + "user?access_token="\
                                    "{access_token}".format(
                                     access_token=self.GITHUB_API_TOKEN)
        requested_user = self.request_url(url, "get")
        github_data = {"github_username": requested_user["login"],
                       "github_user_id": requested_user["id"]}
        return github_data

    def get_repositories(self):
        url = self.GITHUB_API_URL + "user/repos?affiliation=owner,collaborator"
        requested_repositories = self.request_url(url, "get")
        project_repositories = self.repository_requested_repository(
                                    requested_repositories)
        return project_repositories

    def repository_requested_repository(self, resp):
        repositories = {"repositories": []}
        for i, item in enumerate(resp):
            repository_data = {"name": 0, "full_name": 0}
            repository_data["name"] = resp[i]['name']
            repository_data["full_name"] = resp[i]["full_name"]
            repositories["repositories"].append(repository_data)
        return repositories

    def select_repos_by_buttons(self, user):
        received_repositories = self.get_repositories()
        buttons = []
        for repositorio in received_repositories["repositories"]:
            repository_name = repositorio["full_name"]
            if user in repositorio["full_name"]:
                project_name = repositorio["name"]
            else:
                project_name = repositorio["full_name"]
            project_len = len(repository_name.encode('utf-8'))
            if project_len > 54:
                repository_name = repository_name[:51] + "..."
            buttons.append(telegram.InlineKeyboardButton(
                    text=project_name,
                    callback_data="hubrepo: " +
                                  repository_name))
        repo_names = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
        return repo_names

    def register_repo(self, repo_json):
        project_name = repo_json["repository_name"]
        owner = repo_json["owner"]
        chat_id = repo_json["chat_id"]

        user = User.objects(chat_id=chat_id).first()
        try:
            project = Project()
            if user.project:
                webhook = Webhook(chat_id)
                webhook.delete_hook(owner, project_name)
                webhook.delete_hook(user.github_user, user.project.name)
                user.github_user = owner
                user.save()
                project = user.project
                project.update_repository_infos(str(project_name))
            else:
                webhook = Webhook(chat_id)
                webhook.delete_hook(owner, project_name)
                user.github_user = owner
                user.save()
                project.save_repository_infos(user, str(project_name))
            user.save_github_repo_data(project)
        except AttributeError:
            dict_error = {"message":
                          "Tive um erro tentando cadastrar seu repositório. "
                          "Mais tarde você tenta. Ok?"}
            raise AttributeError(json.dumps(dict_error))

    def send_button_message(self, user_infos, chat_id):
        bot = telegram.Bot(token=ACCESS_TOKEN)
        repo_names = self.select_repos_by_buttons(
                     user_infos["github_username"])
        reply_markup = telegram.InlineKeyboardMarkup(repo_names)
        bot.send_message(chat_id=chat_id,
                         text="Encontrei esses repositórios na sua "
                         "conta do GitHub. Qual você quer que eu "
                         "monitore? Clica nele!",
                         reply_markup=reply_markup)

    def compare_repository_name(self, repository_name, repositories):
        for repository in repositories["repositories"]:
            if repository_name in repository["full_name"]:
                return repository["full_name"]
        return repository_name


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
    post_request = post(url=url,
                        headers=header,
                        data=data)
    post_json = post_request.json()
    GITHUB_TOKEN = post_json['access_token']
    return GITHUB_TOKEN


def send_message(token, chat_id):
    access_token = os.environ.get("ACCESS_TOKEN", "")
    bot = telegram.Bot(token=access_token)
    bot.send_message(chat_id=chat_id,
                     text="Você foi cadastrado com sucesso "
                          "no GitHub")
