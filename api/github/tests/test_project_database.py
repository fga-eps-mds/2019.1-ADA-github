from github.data.user import User
from github.data.project import Project
from github.tests.base import BaseTestCase


class TestProject(BaseTestCase):
    def setup(self):
        super().setUp()
        Project.drop_collection()

    def test_create_project(self):
        project = Project()
        description = "Test project"
        name = "Test Project"
        web_url = "https://cakaca.com"
        branches = ["branch1", "branch2"]
        project_id = "2113"

        user = User()
        user.username = "User test create project"
        user.save()

        project.create_project(user, description, name, web_url,
                               branches, project_id)
        project_db = Project.objects(name=name).first()
        self.assertEqual(project, project_db)

    def test_save_repository_infos(self):
        project = Project()
        description = "Test project"
        name = "Test Project"
        web_url = "https://cakaca.com"
        branches = ["branch1", "branch2"]
        project_id = "2113"

        user = User()
        user.username = "User test create project"
        user.save()

        project.create_project(user, description, name, web_url,
                               branches, project_id)
        project.save_repository_infos(user, project.name)
        project_db = Project.objects(name=name).first()
        project_db = Project.objects(name=name).first()
        self.assertEqual(project, project_db)
