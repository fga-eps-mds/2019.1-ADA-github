from github.tests.base import BaseTestCase
from github.find_project_collaborators.utils import FindProjectCollaborators
from github.tests.jsonschemas.find_project_collaborators.schemas import *


class TestFindProjectCollaborators(BaseTestCase):
    def setup(self):
        init_db()
        Project.drop_collection()
        User.drop_collection()

    def test_views_find_collaborators(self):
        pass

    def test_views_find_collaborators_ERROR(self):
        pass

    def test_utils_get_project(self):
        project_name = "2019.1-ADA"
        GITHUB_TOKEN = "?"
        find_project_collaborators = FindProjectCollaborators(GITHUB_TOKEN)
        owner_and_repo = find_project_collaborators.get_project(project_name)
        validate(owner_and_repo, owner_and_repo_schema)

    def test_utils_get_project_ERROR(self):
        pass

    def test_utils_get_collaborators(self):
        pass

    def test_utils_get_collaborators_ERROR(self):
        pass
