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
import base64

from lmcommon.labbook import LabBook
from lmcommon.gitlib import get_git_interface
from lmcommon.configuration import Configuration

from lmsrvcore.auth.user import get_logged_in_user

from lmsrvcore.api import ObjectType
from lmsrvcore.api.interfaces import GitRepository
from lmsrvcore.api.objects import Owner
from lmsrvcore.api.connections import ListBasedConnection

from lmsrvlabbook.api.objects.ref import LabbookRef
from lmsrvlabbook.api.objects.environment import Environment
from lmsrvlabbook.api.objects.note import Note
from lmsrvlabbook.api.connections.ref import LabbookRefConnection
from lmsrvlabbook.api.connections.note import NoteConnection


class LabbookSummary(ObjectType):
    """A type representing a summary of a LabBook used for listing LabBooks

    LabBooks are uniquely identified by both the "owner" and the "name" of the LabBook

    """
    class Meta:
        interfaces = (graphene.relay.Node, GitRepository)

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
            del id_data["type_id"]

        if "username" not in id_data:
            id_data["username"] = get_logged_in_user()

        lb = LabBook()
        lb.from_name(id_data["username"], id_data["owner"], id_data["name"])

        return LabbookSummary(id=Labbook.to_type_id(id_data),
                              name=lb.name, description=lb.description,
                              owner=Owner.create(id_data))


class Labbook(LabbookSummary):
    """A type representing a LabBook and all of its contents

    LabBooks are uniquely identified by both the "owner" and the "name" of the LabBook

    """
    class Meta:
        interfaces = (graphene.relay.Node, GitRepository)

    # The name of the current branch
    active_branch = graphene.Field(LabbookRef)

    # List of branches
    branches = graphene.relay.ConnectionField(LabbookRefConnection)

    # Environment Information
    environment = graphene.Field(Environment)

    # Connection to Note Entries
    notes = graphene.relay.ConnectionField(NoteConnection)

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
            del id_data["type_id"]

        if "username" not in id_data:
            id_data["username"] = get_logged_in_user()

        lb = LabBook()
        lb.from_name(id_data["username"], id_data["owner"], id_data["name"])

        # Get the git information
        if "git" not in id_data:
            git = get_git_interface(Configuration().config["git"])
            git.set_working_directory(os.path.join(git.working_directory,
                                                   id_data["username"],
                                                   id_data["owner"],
                                                   id_data["name"]))
        else:
            git = id_data["git"]

        # Get the current checked out branch name
        id_data["branch"] = git.get_current_branch_name()

        # Share git instance to speed up IO
        id_data["git"] = git

        return Labbook(id=Labbook.to_type_id(id_data),
                       name=lb.name, description=lb.description,
                       owner=Owner.create(id_data),
                       active_branch=LabbookRef.create(id_data),
                       environment=Environment.create(id_data))

    def resolve_branches(self, args, context, info):
        """Method to page through branch Refs

        Args:
            args:
            context:
            info:

        Returns:

        """
        # Get the git information
        git = get_git_interface(Configuration().config["git"])
        # TODO: Fix assumption that loading logged in user. Need to parse data from original request if username
        git.set_working_directory(os.path.join(git.working_directory, get_logged_in_user(),
                                               self.owner.username, self.name))

        # TODO: Design a better cursor implementation
        # Get all edges and cursors. Here, cursors are just an index into the refs
        edges = [x for x in git.repo.refs]
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, args)
        lbc.apply()

        # Get LabbookRef instances
        edge_objs = []
        for edge, cursor in zip(lbc.edges, lbc.cursors):
            parts = edge.name.split("/")
            if len(parts) > 1:
                prefix = parts[0]
                branch = parts[1]
            else:
                prefix = None
                branch = parts[0]

            id_data = {"name": self.name,
                       "owner": self.owner.username,
                       "prefix": prefix,
                       "branch": branch}
            edge_objs.append(LabbookRefConnection.Edge(node=LabbookRef.create(id_data), cursor=cursor))

        return LabbookRefConnection(edges=edge_objs,
                                    page_info=lbc.page_info)

    def resolve_notes(self, args, context, info):
        """Method to page through branch Refs

        Args:
            args:
            context:
            info:

        Returns:

        """
        # TODO: Fix assumption that loading logged in user. Need to parse data from original request if username
        # Load LabBook instance
        lb = LabBook()
        lb.from_name(get_logged_in_user(), self.owner.username, self.name)

        # TODO: Design a better cursor implementation that actually pages through repo history
        # retrieve a list of notes from the commit log.
        labbook_log_data = lb.log(max_count=100)

        # Get all edges and cursors. Here, cursors are just an index into the refs
        edges = [x for x in labbook_log_data]
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, args)
        lbc.apply()

        # Get LabbookRef instances
        edge_objs = []
        for edge, cursor in zip(lbc.edges, lbc.cursors):
            #TODO: need to index into commit history better, this hack skips commits not in db. Probably should use DB
            # directly vs. the git log
            if edge["committer"]["name"] != 'Gigantum AutoCommit':
                continue

            id_data = {"name": self.name,
                       "owner": self.owner.username,
                       "commit": edge["commit"]}
            edge_objs.append(NoteConnection.Edge(node=Note.create(id_data), cursor=cursor))

        return NoteConnection(edges=edge_objs, page_info=lbc.page_info)
