from github.tests.base import BaseTestCase
from github.find_project_collaborators.utils import FindProjectCollaborators
from github.tests.jsonschemas.find_project_collaborators.schemas import \
     owner_and_repo_schema
from github.data.user import User
from github.data.project import Project
import os
import json
from jsonschema import validate
from requests.exceptions import HTTPError


class TestFindProjectCollaborators(BaseTestCase):
    access_token = os.getenv("GITHUB_API_TOKEN", "")

    def setup(self):
        super.setup()
        Project.drop_collection()
        User.drop_collection()

    #def test_views_find_collaborators(self):
    #    pass

    #def test_views_find_collaborators_ERROR(self):
    #    pass

    #def test_utils_get_project(self):
    #    #chat_id = "987654321"
    #    #user = User.objects(chat_id=chat_id).first()
    #    #project = user.project
    #    #project_name = project.name
    #    user = User()
    #    project = Project()
    #    user.project = project
    #    user.project.name = "TEP"
    #    user.access_token = self.access_token
    #    #project_name = "TEP"
    #    print("#"*10+"\n"+user.access_token+"\n"+"#"*10, file=sys.stderr)
    #    project.save()
    #    user.save()
    #    find_project_collaborators = FindProjectCollaborators(user.access_token)
    #    owner_and_repo = find_project_collaborators.get_project(project_name)
    #    validate(owner_and_repo, owner_and_repo_schema)

    def test_utils_get_project_ERROR(self):  # esse teste taokey
        user = User()
        project = Project()
        user.project = project
        user.project.name = "TEP"
        user.access_token = "errroouu"
        project.save()
        user.save()
        find_project_collaborators = FindProjectCollaborators(
                                     user.access_token)
        with self.assertRaises(HTTPError) as context:
            find_project_collaborators.get_project(user.project.name)
        unauthorized_json = json.loads(str(context.exception))
        self.assertIsInstance(unauthorized_json["status_code"], int)

    #def test_utils_get_collaborators(self):
    #    user = User()
    #    #project = Project()
    #    #user.project = project
    #    #user.project.name = "TEP"
    #    user.access_token = self.access_token
    #    owner_and_repo = "sudjoao/TEP"
    #    #project_name = "TEP"
    #    print("#"*10+"\n"+user.access_token+"\n"+"#"*10, file=sys.stderr)
    #    #project.save()
    #    user.save()
    #    find_project_collaborators= FindProjectCollaborators(user.access_token)
    #    contributors_names= find_project_collaborators.\
    #    get_collaborators(owner_and_repo)
    #    self.assertIsInstance(contributors_names, list)

    def test_utils_get_collaborators_ERROR(self):  # esse teste taokey
        user = User()
        user.access_token = "erroouu"
        owner_and_repo = "sudjoao/TEP"
        user.save()
        find_project_collaborators = FindProjectCollaborators(
                                     user.access_token)
        with self.assertRaises(HTTPError) as context:
            find_project_collaborators.get_collaborators(owner_and_repo)
        unauthorized_json = json.loads(str(context.exception))
        self.assertIsInstance(unauthorized_json["status_code"], int)
