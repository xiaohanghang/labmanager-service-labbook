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

from lmsrvlabbook.api.objects import LabbookCommit, LabbookRef, LabbookRefConnection


class Labbook(ObjectType):
    """A type representing a LabBook and all of its contents

    LabBooks are uniquely identified by both the "owner" and the "name" of the LabBook

    """
    class Meta:
        interfaces = (graphene.relay.Node, GitRepository)

    # The name of the current branch
    active_branch = graphene.Field(LabbookRef)

    # List of branches
    branches = graphene.relay.ConnectionField(LabbookRefConnection)

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
            del id_data["type_id"]

        if "username" not in id_data:
            id_data["username"] = get_logged_in_user()

        lb = LabBook()
        lb.from_name(id_data["username"], id_data["owner"], id_data["name"])

        # Get the git information
        git = get_git_interface(Configuration().config["git"])
        git.set_working_directory(os.path.join(git.working_directory, id_data["username"],
                                               id_data["owner"], id_data["name"]))

        # Get the current checked out branch name
        id_data["branch"] = git.get_current_branch_name()

        # Share git instance to speed up IO
        id_data["git"] = git

        # Get branches
        #branch_listing = git.list_branches()

        return Labbook(id=Labbook.to_type_id(id_data),
                       name=lb.name, description=lb.description,
                       owner=Owner.create(id_data),
                       active_branch=LabbookRef.create(id_data))

    def resolve_branches(self, args, context, info):
        """Method to page through branch Refs

        Args:
            args:
            context:
            info:

        Returns:

        """
        if "first" in args:
            if int(args["first"]) < 0:
                raise ValueError("`first` must be greater than 0")
        if "last" in args:
            if int(args["last"]) < 0:
                raise ValueError("`last` must be greater than 0")

        # Get the git information
        git = get_git_interface(Configuration().config["git"])
        # TODO: Fix assumption that loading logged in user. Need to parse data from original request if username
        git.set_working_directory(os.path.join(git.working_directory, get_logged_in_user(),
                                               self.owner.username, self.name))

        # TODO: Design a better cursor implementation
        # Get all edges and cursors. Here, cursors are just an index into the refs
        edges = [x for x in git.repo.refs]
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt,x in enumerate(edges)]

        after_index = None
        before_index = None
        if "after" in args:
            if args["after"] in cursors:
                # Remove edges after cursor
                after_index = int(base64.b64decode(args["after"]))

        if "before" in args:
            if args["before"] in cursors:
                # Remove edges after cursor
                before_index = int(base64.b64decode(args["before"]))

        if after_index is not None and before_index is not None:
            edges = edges[after_index+1:before_index]
            cursors = cursors[after_index+1:before_index]
        elif after_index is not None:
            edges = edges[after_index + 1:]
            cursors = cursors[after_index + 1:]
        elif before_index is not None:
            edges = edges[:before_index]
            cursors = cursors[:before_index]

        num_edges_before_slice = len(edges)

        if "first" in args:
            if len(edges) > int(args["first"]):
                edges = edges[:int(args["first"])]
                cursors = cursors[:int(args["first"])]

        if "last" in args:
            if len(edges) > int(args["last"]):
                edges = edges[-int(args["last"]):]
                cursors = cursors[-int(args["last"]):]

        # Get LabbookRef instances
        edge_objs = []
        for edge, cursor in zip(edges, cursors):
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

        # Compute page info status
        has_previous_page = False
        if "last" not in args:
            has_previous_page = False
        elif num_edges_before_slice > int(args["last"]):
            has_previous_page = True

        has_next_page = False
        if "first" not in args:
            has_next_page = False
        elif num_edges_before_slice > int(args["first"]):
            has_next_page = True

        return LabbookRefConnection(edges=edge_objs,
                                    page_info=graphene.relay.PageInfo(has_next_page=has_next_page,
                                                                      has_previous_page=has_previous_page))


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
