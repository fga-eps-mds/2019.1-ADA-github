import mongoengine
from github.data import init_db
from github.data.project import Project


class User(mongoengine.Document):
    init_db()
    project = mongoengine.ReferenceField(Project)
    access_token = mongoengine.StringField(max_length=100)
    github_user = mongoengine.StringField(max_length=100)
    chat_id = mongoengine.StringField(max_length=100)
    github_user_id = mongoengine.StringField(max_length=100)
    meta = {
        'db_alias': 'AdaGitHub',
        'collection': 'User'
    }

    def create_user(self, username):
        self.github_user = username
        self.save()
        return self

    def save_github_user_data(self, github_user, github_user_id, chat_id):
        self.github_user = github_user
        self.github_user_id = github_user_id
        self.chat_id = chat_id
        self.save()
        return self

    def save_github_repo_data(self, project):
        self.project = project
        self.update(project=project)
        return self
