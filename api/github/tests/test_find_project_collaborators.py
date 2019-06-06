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
import requests
import sys


class TestFindProjectCollaborators(BaseTestCase):
    access_token = os.getenv("GITHUB_API_TOKEN", "")

    def setup(self):
        super.setup()
        Project.drop_collection()
        User.drop_collection()

    #def test_views_find_collaborators(self):
    #    chat_id = "987654321"
    #    #user = User.objects(chat_id=chat_id).first()
    #    #project = user.project
    #    #project_name = project.name
    #    user = User()
    #    project = Project()
    #    user.project = project
    #    user.project.name = "TEP"
    #    user.access_token = self.access_token
    #    user.chat_id = chat_id
    #    #project_name = "TEP"
    #    print("#"*10+"\n"+user.access_token+"\n"+"#"*10, file=sys.stderr)
    #    project.save()
    #    user.save()
    #    response = self.client.get("/api/find_collaborators/" +
    #                               "{chat_id}".format(chat_id=user.chat_id))
    #    self.assertEqual(response.status_code, 200)

    def test_views_find_collaborators_ERROR(self):
        chat_id = "987654321"
        #user = User.objects(chat_id=chat_id).first()
        #project = user.project
        #project_name = project.name
        user = User()
        project = Project()
        user.project = project
        user.project.name = "TEP"
        user.access_token = "errroouu"
        user.chat_id = chat_id
        #project_name = "TEP"
        print("#"*10+"\n"+user.access_token+"\n"+"#"*10, file=sys.stderr)
        project.save()
        user.save()
        with self.assertRaises(HTTPError) as context:
            try:
                response = requests.get("http://localhost:5015/api/"+
                                        "find_collaborators/{chat_id}".format(
                                        chat_id=user.chat_id))
                response.raise_for_status()
            except HTTPError as http_error:
                dict_message = json.loads(str(http_error))
            #except AttributeError as atribute_error:
            #    dict_message = json.loads(str(atribute_error))
        unauthorized_json = json.loads(str(context.exception))
        self.assertIsInstance(unauthorized_json["status_code"], int)


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

    #def test_utils_get_project_ERROR(self):  # esse teste taokey
    #    user = User()
    #    project = Project()
    #    user.project = project
    #    user.project.name = "TEP"
    #    user.access_token = "errroouu"
    #    project.save()
    #    user.save()
    #    find_project_collaborators = FindProjectCollaborators(
    #                                 user.access_token)
    #    with self.assertRaises(HTTPError) as context:
    #        find_project_collaborators.get_project(user.project.name)
    #    unauthorized_json = json.loads(str(context.exception))
    #    self.assertIsInstance(unauthorized_json["status_code"], int)

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

    #def test_utils_get_collaborators_ERROR(self):  # esse teste taokey
    #    user = User()
    #    user.access_token = "erroouu"
    #    owner_and_repo = "sudjoao/TEP"
    #    user.save()
    #    find_project_collaborators = FindProjectCollaborators(
    #                                 user.access_token)
    #    with self.assertRaises(HTTPError) as context:
    #        find_project_collaborators.get_collaborators(owner_and_repo)
    #    unauthorized_json = json.loads(str(context.exception))
    #    self.assertIsInstance(unauthorized_json["status_code"], int)
