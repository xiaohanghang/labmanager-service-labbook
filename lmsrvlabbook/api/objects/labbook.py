# Copyright (c) 2017 FlashX, LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import graphene
import os

from lmcommon.labbook import LabBook
from lmcommon.gitlib import get_git_interface
from lmcommon.configuration import Configuration

from lmsrvcore.auth.user import get_logged_in_user

from lmsrvcore.api import ObjectType
from lmsrvcore.api.interfaces import GitRepository
from lmsrvcore.api.objects import Owner

from lmsrvlabbook.api.objects import LabbookCommit, LabbookRef


class Labbook(ObjectType):
    """A type representing a LabBook and all of its contents

    LabBooks are uniquely identified by both the "owner" and the "name" of the LabBook

    """
    class Meta:
        interfaces = (graphene.relay.Node, GitRepository)

    ## The name of the current branch
    #active_branch = graphene.Field(LabbookRef)
#
    ##TODO UPDATE TO CONNECTIONS
    ## Connection to access local branches
    #local_branches = graphene.List(graphene.String)
#
    ## Connection to access remote branches
    #remote_branches = graphene.List(graphene.String)
#
    ## The git commit of the currently checked out branch
    #commit = graphene.Field(LabbookCommit)

    @staticmethod
    def get_node(node_id, context, info):
        input_data = {"type_id": node_id}
        return Labbook.create(input_data)

    @staticmethod
    def to_type_id(id_data):
        """Method to generate a single string that uniquely identifies this object

        Args:
            id_data(dict):

        Returns:
            str
        """
        return "{}&{}".format(id_data["owner"], id_data["name"])

    @staticmethod
    def parse_type_id(type_id):
        """Method to parse an ID for a given type into its identifiable variables returned as a dictionary of strings

        Args:
            type_id (str): type unique identifier

        Returns:
            dict
        """
        split = type_id.split("&")
        return {"owner": split[0], "name": split[1]}

    @staticmethod
    def create(id_data):
        """Method to create a graphene LabBook object based on the node ID or owner+name

        id_data should at a minimum contain either `type_id` or `owner` & `name`

            {
                "type_id": <unique id for this object Type),
                "owner": <owner username (or org)>,
                "name": <name of the labbook>
            }

        Args:
            id_data(dict): A dictionary of variables that uniquely ID the instance. Can be a node ID or other vars

        Returns:
            Labbook
        """
        if "type_id" in id_data:
            id_data.update(Labbook.parse_type_id(id_data["type_id"]))

        if "username" not in id_data:
            id_data["username"] = get_logged_in_user()

        lb = LabBook()
        lb.from_name(id_data["username"], id_data["owner"], id_data["name"])

        # Get the git information
        git = get_git_interface(Configuration().config["git"])
        git.set_working_directory(os.path.join(git.working_directory, id_data["username"],
                                               id_data["owner"], id_data["name"]))

        # Get branches
        branch_listing = git.list_branches()

        return Labbook(name=lb.name, description=lb.description,
                       owner=Owner.create({"username": lb.owner["username"]}),
                       id=Labbook.to_type_id(id_data))
                       #commit=_get_graphene_labbook_commit(lb))
                       #id=lb.id,
                       #local_branches=branch_listing["local"], remote_branches=branch_listing["remote"],
                       #active_branch=_get_graphene_labbook_ref(lb, git_obj=git))


class CreateLabbook(graphene.Mutation):
    """Mutator for creation of a new Labbook on disk"""

    class Input:
        name = graphene.String()
        description = graphene.String()

    # Return the LabBook instance
    labbook = graphene.Field(lambda: Labbook)

    @staticmethod
    def mutate(root, args, context, info):
        # TODO: Lookup name based on logged in user when available
        username = get_logged_in_user()

        # Create a new empty LabBook
        lb = LabBook()
        lb.new(username=username,
               name=args.get('name'),
               description=args.get('description'),
               owner={"username": username})

        # Get a graphene instance of the newly created LabBook
        id_data = {"owner": username,
                   "name": lb.name,
                   "username": username}
        new_labbook = Labbook.create(id_data)
        return CreateLabbook(labbook=new_labbook)


#SNIPPET FOR GETTING REFS
# # Get the commit information
#        git = get_git_interface(Configuration().config["git"])
#        git.set_working_directory(os.path.join(git.working_directory,
#                                               id_data["username"],
#                                               id_data["owner"],
#                                               id_data["name"]))
#
#        return LabbookRef(commit=_get_graphene_labbook_commit(labbook_obj),
#                          name=git_obj.get_current_branch_name(), prefix=git_obj.git_path.rsplit("/", 1)[0])
#