# Copyright (c) 2018 FlashX, LLC
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
import graphene

from lmsrvlabbook.api.connections.labbook import LabbookConnection, Labbook
from lmsrvlabbook.api.connections.remotelabbook import RemoteLabbookConnection, RemoteLabbook

from lmcommon.labbook import LabBook
from lmcommon.configuration import Configuration
from lmcommon.gitlib.gitlab import GitLabManager

from lmsrvcore.auth.user import get_logged_in_username
from lmsrvcore.api.connections import ListBasedConnection
from lmsrvcore.auth.identity import parse_token


class LabbookList(graphene.ObjectType, interfaces=(graphene.relay.Node,)):
    """A type simply used as a container to group local and remote LabBooks for better relay support

    Labbook and RemoteLabbook objects are uniquely identified by both the "owner" and the "name" of the LabBook

    NOTE: RemoteLabbooks require all fields to be explicitly set as there is no current way to asynchronously retrieve
          the data

    NOTE: Currently all RemoteLabbook description fields will return empty strings

    """
    # Connection to locally available labbooks
    local_labbooks = graphene.relay.ConnectionField(LabbookConnection,
                                                    sort=graphene.String(default_value="az"),
                                                    reverse=graphene.Boolean(default_value=False))

    # Connection to remotely available labbooks
    remote_labbooks = graphene.relay.ConnectionField(RemoteLabbookConnection,
                                                     sort=graphene.String(default_value="az"),
                                                     reverse=graphene.Boolean(default_value=False))

    @classmethod
    def get_node(cls, info, id):
        """Method to resolve the object based on it's Node ID"""
        # This object doesn't really have a node because it's simply container
        return LabbookList(id=id)

    def resolve_id(self, info):
        """Resolve the unique Node id for this object"""
        # This object doesn't really have a node because it's simply container
        return ""

    def resolve_local_labbooks(self, info, sort: str, reverse: bool, **kwargs):
        """Method to return all graphene Labbook instances for the logged in user available locally

        Uses the "currently logged in" user

        Args:
            sort(sort_mode): String specifying how labbooks should be sorted
            reverse(bool): Reverse sorting if True

        Returns:
            list(Labbook)
        """
        lb = LabBook()

        username = get_logged_in_username()

        # Collect all labbooks for all owners
        edges = lb.list_local_labbooks(username=username, sort_mode=sort, reverse=reverse)
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, kwargs)
        lbc.apply()

        # Get Labbook instances
        edge_objs = []
        for edge, cursor in zip(lbc.edges, lbc.cursors):
            create_data = {"id": "{}&{}".format(edge["owner"], edge["name"]),
                           "name": edge["name"],
                           "owner": edge["owner"]}

            edge_objs.append(LabbookConnection.Edge(node=Labbook(**create_data),
                                                    cursor=cursor))

        return LabbookConnection(edges=edge_objs, page_info=lbc.page_info)

    def resolve_remote_labbooks(self, info, sort: str, reverse: bool, **kwargs):
        """Method to return a all RemoteLabbook instances for the logged in user

        This is a remote call, so should be fetched on its own and only when needed. The user must have a valid
        session for data to be returned.

        It is recommended to use large page size (e.g. 50-100). This is due to how the remote server returns all the
        available data at once, so it is more efficient to load a lot of records at a time.

        Args:
            sort(sort_mode): String specifying how labbooks should be sorted
            reverse(bool): Reverse sorting if True

        Supported sorting modes:
            - az: naturally sort
            - created_on: sort by creation date, newest first
            - modified_on: sort by modification date, newest first

        Returns:
            list(Labbook)
        """
        # Load config data
        configuration = Configuration().config

        # Extract valid Bearer token
        token = None
        if hasattr(info.context.headers, 'environ'):
            if "HTTP_AUTHORIZATION" in info.context.headers.environ:
                token = parse_token(info.context.headers.environ["HTTP_AUTHORIZATION"])
        if not token:
            raise ValueError("Authorization header not provided. Cannot list remote LabBooks.")

        # Get remote server configuration
        default_remote = configuration['git']['default_remote']
        admin_service = None
        for remote in configuration['git']['remotes']:
            if default_remote == remote:
                admin_service = configuration['git']['remotes'][remote]['admin_service']
                break

        if not admin_service:
            raise ValueError('admin_service could not be found')

        # Query backend for data
        mgr = GitLabManager(default_remote, admin_service, access_token=token)
        edges = mgr.list_labbooks(sort_mode=sort, reverse=reverse)
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, kwargs)
        lbc.apply()

        # Get Labbook instances
        edge_objs = []
        for edge, cursor in zip(lbc.edges, lbc.cursors):
            create_data = {"id": "{}&{}".format(edge["namespace"], edge["labbook_name"]),
                           "name": edge["labbook_name"],
                           "owner": edge["namespace"],
                           "description": edge["description"],
                           "creation_date_utc": edge["created_on"],
                           "modified_date_utc": edge["modified_on"]}

            edge_objs.append(RemoteLabbookConnection.Edge(node=RemoteLabbook(**create_data),
                                                          cursor=cursor))

        return RemoteLabbookConnection(edges=edge_objs, page_info=lbc.page_info)