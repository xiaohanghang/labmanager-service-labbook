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
import base64
import json
import graphene
import copy

import os

from lmcommon.configuration import Configuration
from lmcommon.logging import LMLogger
from lmcommon.gitlib import get_git_interface
from lmcommon.labbook import LabBook
from lmcommon.activity import ActivityStore
from lmcommon.gitlib.gitlab import GitLabRepositoryManager

from lmsrvcore.auth.user import get_logged_in_username

from lmsrvcore.api import ObjectType, logged_query
from lmsrvcore.api.connections import ListBasedConnection
from lmsrvcore.api.interfaces import GitRepository
from lmsrvcore.api.objects import Owner
from lmsrvcore.auth.identity import parse_token

from lmsrvlabbook.api.connections.ref import LabbookRefConnection
from lmsrvlabbook.api.objects.environment import Environment
from lmsrvlabbook.api.objects.ref import LabbookRef
from lmsrvlabbook.api.objects.labbooksection import LabbookSection
from lmsrvlabbook.api.connections.activity import ActivityConnection
from lmsrvlabbook.api.objects.activity import ActivityDetailObject, ActivityRecordObject

logger = LMLogger.get_logger()


class Labbook(ObjectType):
    """A type representing a LabBook and all of its contents

    LabBooks are uniquely identified by both the "owner" and the "name" of the LabBook

    """
    class Meta:
        interfaces = (graphene.relay.Node, GitRepository)

    # The name of the current branch
    active_branch = graphene.Field(LabbookRef)

    # Get the URL of the remote origin
    default_remote = graphene.String()

    # List of branches
    branches = graphene.relay.ConnectionField(LabbookRefConnection)

    # List of collaborators
    collaborators = graphene.List(graphene.String)

    # A boolean indicating if the current user can manage collaborators
    can_manage_collaborators = graphene.Boolean()

    # How many commits the current active_branch is behind remote (0 if up-to-date or local-only).
    updates_available_count = graphene.Int()

    # Whether repo state is clean
    is_repo_clean = graphene.Boolean()

    # Environment Information
    environment = graphene.Field(Environment)

    # List of sections
    code = graphene.Field(LabbookSection)
    input = graphene.Field(LabbookSection)
    output = graphene.Field(LabbookSection)

    # Connection to Activity Entries
    activity_records = graphene.relay.ConnectionField(ActivityConnection)

    # Access a detail record directly, which is useful when fetching detail items
    detail_record = graphene.Field(ActivityDetailObject, key=graphene.String())
    detail_records = graphene.List(ActivityDetailObject, keys=graphene.List(graphene.String))

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

    # @BVB - this decorator breaks things, with the error that the argument "self" is missing. Possibly because static?
    # @logged_query
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
            id_data["username"] = get_logged_in_username()

        lb = LabBook()
        lb.from_name(id_data["username"], id_data["owner"], id_data["name"])
        id_data["labbook_instance"] = lb

        return Labbook(id=Labbook.to_type_id(id_data),
                       name=lb.name, description=lb.description,
                       owner=Owner.create(id_data), environment=Environment.create(id_data),
                       _id_data=id_data)

    def resolve_updates_available_count(self, args, context, info):
        """Get number of commits the active_branch is behind its remote counterpart.
        Returns 0 if up-to-date or if local only."""
        lb = LabBook()
        lb.from_name(get_logged_in_username(), self.owner.username, self.name)

        # Note, by default using remote "origin"
        return lb.get_commits_behind_remote("origin")[1]

    def resolve_active_branch(self, args, context, info):
        """Method to get the active branch

        Args:
            args:
            context:
            info:

        Returns:

        """
        lb = LabBook()
        lb.from_name(get_logged_in_username(), self.owner.username, self.name)

        # Get the current checked out branch name
        self._id_data["branch"] = lb.git.get_current_branch_name()

        return LabbookRef.create(self._id_data)

    def resolve_is_repo_clean(self, args, context, info):
        """Return True if no untracked files and no uncommitted changes (i.e., Git repo clean)

        Args:
            args:
            context:
            info:

        Returns:

        """
        lb = LabBook()
        lb.from_name(get_logged_in_username(), self.owner.username, self.name)

        try:
            return lb.is_repo_clean
        except Exception as e:
            logger.exception(e)
            raise

    def resolve_default_remote(self, args, context, info):
        """Return True if no untracked files and no uncommitted changes (i.e., Git repo clean)

        Args:
            args:
            context:
            info:

        Returns:

        """
        lb = LabBook()
        lb.from_name(get_logged_in_username(), self.owner.username, self.name)

        try:
            remotes = lb.git.list_remotes()
            if remotes:
                url = [x['url'] for x in remotes if x['name'] == 'origin']
                if url:
                    return url[0]
                else:
                    logger.warning(f"There exist remotes in {str(lb)}, but no origin found.")
            return None
        except Exception as e:
            logger.exception(e)
            raise

    def resolve_branches(self, args, context, info):
        """Method to page through branch Refs

        Args:
            args:
            context:
            info:

        Returns:

        """
        lb = LabBook()
        lb.from_name(get_logged_in_username(), self.owner.username, self.name)

        try:
            # Get all edges and cursors. Here, cursors are just an index into the refs
            edges = [x for x in lb.git.repo.refs]
            cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt,
                                                                                              x in enumerate(edges)]

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

                id_data = {"name": lb.name,
                           "owner": lb.owner['username'],
                           "prefix": prefix,
                           "branch": branch}
                edge_objs.append(LabbookRefConnection.Edge(node=LabbookRef.create(id_data), cursor=cursor))

            return LabbookRefConnection(edges=edge_objs,
                                        page_info=lbc.page_info)
        except Exception as e:
            logger.exception(e)
            raise

    def resolve_code(self, args, context, info):
        """Method to resolve the code section"""
        # Make a copy of id_data and set the section to code
        if "labbook_instance" not in self._id_data:
            lb = LabBook()
            lb.from_name(self._id_data["username"], self._id_data["owner"], self._id_data["name"])
            self._id_data["labbook_instance"] = lb

        local_id_data = copy.deepcopy(self._id_data)
        local_id_data['section'] = 'code'

        return LabbookSection(id=LabbookSection.to_type_id(local_id_data),
                              _id_data=local_id_data)

    def resolve_input(self, args, context, info):
        """Method to resolve the output section"""
        # Make a copy of id_data and set the section to code
        if "labbook_instance" not in self._id_data:
            lb = LabBook()
            lb.from_name(self._id_data["username"], self._id_data["owner"], self._id_data["name"])
            self._id_data["labbook_instance"] = lb

        local_id_data = copy.deepcopy(self._id_data)
        local_id_data['section'] = 'input'

        return LabbookSection(id=LabbookSection.to_type_id(local_id_data),
                              _id_data=local_id_data)

    def resolve_output(self, args, context, info):
        """Method to resolve the output section"""
        # Make a copy of id_data and set the section to code
        if "labbook_instance" not in self._id_data:
            lb = LabBook()
            lb.from_name(self._id_data["username"], self._id_data["owner"], self._id_data["name"])
            self._id_data["labbook_instance"] = lb

        local_id_data = copy.deepcopy(self._id_data)
        local_id_data['section'] = 'output'

        return LabbookSection(id=LabbookSection.to_type_id(local_id_data),
                              _id_data=local_id_data)

    def resolve_activity_records(self, args, context, info):
        """Method to page through branch Refs

        Args:
            args:
            context:
            info:

        Returns:

        """
        # Make a copy of id_data and set the section to code
        if "labbook_instance" not in self._id_data:
            lb = LabBook()
            lb.from_name(self._id_data["username"], self._id_data["owner"], self._id_data["name"])
            self._id_data["labbook_instance"] = lb

        store = ActivityStore(self._id_data["labbook_instance"])

        if args.get('before') or args.get('last'):
            raise ValueError("Only `after` and `first` arguments are supported when paging activity records")

        # Get edges and cursors
        edges = store.get_activity_records(after=args.get('after'), first=args.get('first'))
        if edges:
            cursors = [x.commit for x in edges]
        else:
            cursors = []

        # Get ActivityRecordObject instances
        edge_objs = []
        for edge, cursor in zip(edges, cursors):
            edge_objs.append(ActivityConnection.Edge(node=ActivityRecordObject.from_activity_record(edge, store),
                                                     cursor=cursor))

        # Create page info based on first commit. Since only paging backwards right now, just check for commit
        if edges:
            first_commit = self._id_data["labbook_instance"].git.repo.git.rev_list('HEAD', max_parents=0)
            if edges[-1].linked_commit == first_commit:
                has_next_page = False
            else:
                has_next_page = True

            end_cursor = cursors[-1]
        else:
            has_next_page = False
            end_cursor = None

        page_info = graphene.relay.PageInfo(has_next_page=has_next_page, has_previous_page=False, end_cursor=end_cursor)

        return ActivityConnection(edges=edge_objs, page_info=page_info)

    def resolve_detail_record(self, args, context, info):
        """Method to page through branch Refs

        Args:
            args:
            context:
            info:

        Returns:

        """
        # Make a copy of id_data and set the section to code
        if "labbook_instance" not in self._id_data:
            lb = LabBook()
            lb.from_name(self._id_data["username"], self._id_data["owner"], self._id_data["name"])
            self._id_data["labbook_instance"] = lb

        store = ActivityStore(self._id_data["labbook_instance"])
        detail_record = store.get_detail_record(args.get('key'))

        return ActivityDetailObject.from_detail_record(detail_record, store)

    def resolve_detail_records(self, args, context, info):
        """Method to page through branch Refs

        Args:
            args:
            context:
            info:

        Returns:

        """
        # Make a copy of id_data and set the section to code
        if "labbook_instance" not in self._id_data:
            lb = LabBook()
            lb.from_name(self._id_data["username"], self._id_data["owner"], self._id_data["name"])
            self._id_data["labbook_instance"] = lb

        store = ActivityStore(self._id_data["labbook_instance"])
        detail_records = [store.get_detail_record(x) for x in args.get('keys')]

        return [ActivityDetailObject.from_detail_record(x, store) for x in detail_records]

    def resolve_collaborators(self, args, context, info):
        """Method to get the list of collaborators for a labbook

        Args:
            args:
            context:
            info:

        Returns:

        """
        lb = LabBook()
        lb.from_name(get_logged_in_username(), self.owner.username, self.name)

        # TODO: Future work will look up remote in LabBook data, allowing user to select remote.
        default_remote = lb.labmanager_config.config['git']['default_remote']
        admin_service = None
        for remote in lb.labmanager_config.config['git']['remotes']:
            if default_remote == remote:
                admin_service = lb.labmanager_config.config['git']['remotes'][remote]['admin_service']
                break

        # Extract valid Bearer token
        if "HTTP_AUTHORIZATION" in context.headers.environ:
            token = parse_token(context.headers.environ["HTTP_AUTHORIZATION"])
        else:
            raise ValueError("Authorization header not provided. Must have a valid session to query for collaborators")

        # Get collaborators from remote service
        mgr = GitLabRepositoryManager(default_remote, admin_service, token,
                                      self._id_data["username"], self._id_data["owner"], self._id_data["name"])
        try:
            collaborators = mgr.get_collaborators()
        except ValueError:
            # If ValueError Raised, assume repo doesn't exist yet
            return []

        return [x[1] for x in collaborators]

    def resolve_can_manage_collaborators(self, args, context, info):
        """Method to get the list of collaborators for a labbook

        Args:
            args:
            context:
            info:

        Returns:

        """
        lb = LabBook()
        lb.from_name(get_logged_in_username(), self.owner.username, self.name)

        # TODO: Future work will look up remote in LabBook data, allowing user to select remote.
        default_remote = lb.labmanager_config.config['git']['default_remote']
        admin_service = None
        for remote in lb.labmanager_config.config['git']['remotes']:
            if default_remote == remote:
                admin_service = lb.labmanager_config.config['git']['remotes'][remote]['admin_service']
                break

        # Extract valid Bearer token
        if "HTTP_AUTHORIZATION" in context.headers.environ:
            token = parse_token(context.headers.environ["HTTP_AUTHORIZATION"])
        else:
            raise ValueError("Authorization header not provided. Must have a valid session to query for collaborators")

        # Get collaborators from remote service
        mgr = GitLabRepositoryManager(default_remote, admin_service, token,
                                      self._id_data["username"], self._id_data["owner"], self._id_data["name"])
        try:
            collaborators = mgr.get_collaborators()
        except ValueError:
            # If ValueError Raised, assume repo doesn't exist yet
            return False

        can_manage = False
        for c in collaborators:
            if c[1] == self._id_data["username"]:
                if c[2] is True:
                    can_manage = True

        return can_manage
