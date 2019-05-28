from github.data.user import User
from github.data.project import Project
from github.tests.base import BaseTestCase


class TestUserDatabase(BaseTestCase):
    def setup(self):
        super().setUp()
        User.drop_collection()

    def test_create_user(self):
        user = User()
        username = "teste_User"
        user.create_user(username)
        user2 = User.objects(github_user=username).first()
        self.assertEqual(user, user2)

    def test_save_github_repo_data(self):
        user = User()
        username = "teste_User"
        user.create_user(username)

        project = Project()
        project.user_id = user.id
        project.save()

        user.save_github_repo_data(project)

        project_user = User.objects(project=project).first()
        self.assertEqual(user, project_user)

    def test_save_github_user_data(self):
        User.drop_collection()
        github_user = 'git_user'
        chat_id = 'id'
        github_user_id = 'git_id'
        user = User()
        user.github_user = github_user
        user.save()
        user.save_github_user_data(github_user, chat_id, github_user_id)

        user_db = User.objects(github_user=github_user).first()
        self.assertEqual(user, user_db)
