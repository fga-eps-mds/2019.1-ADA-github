import mongoengine
from github.data import init_db


class Project(mongoengine.Document):
    user_id = mongoengine.ObjectIdField(required=False)
    description = mongoengine.StringField(max_length=100)
    name = mongoengine.StringField(max_length=100)
    svn_url = mongoengine.URLField()
    branches = mongoengine.ListField()
    project_id = mongoengine.StringField(max_length=100)
    init_db()
    meta = {
        'db_alias': 'AdaGitHub',
        'collection': 'Project'
    }

    def create_project(self, user, description, name,
                       web_url, branches, project_id):
        self.user_id = user.id
        self.description = description
        self.name = name
        self.web_url = web_url
        self.branches = branches
        self.project_id = project_id
        self.save()
        return self

    def save_repository_infos(self, user, name):

        self.user_id = user.id
        self.name = name
        self.save()
        return self

    def update_repository_infos(self, name):
        self.update(name=name)
        return self
