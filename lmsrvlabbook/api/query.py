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
import graphene
from graphene import resolve_only_args

from lmcommon.labbook import LabBook

from lmsrvcore.auth.user import get_logged_in_user
from lmsrvcore.api.connections import ListBasedConnection

from lmsrvlabbook.api.objects.labbook import Labbook, LabbookSummary
from lmsrvlabbook.api.connections.labbook import LabbookConnection


class LabbookQuery(graphene.AbstractType):
    """Entry point for all LabBook queryable fields"""
    # Node Fields for Relay
    node = graphene.relay.Node.Field()

    labbook = graphene.Field(Labbook, owner=graphene.String(), name=graphene.String())

    # Connection to locally available labbooks
    local_labbooks = graphene.relay.ConnectionField(LabbookConnection)

    @resolve_only_args
    def resolve_labbook(self, owner, name):
        """Method to return a graphene Labbok instance based on the name

        Uses the "currently logged in" user

        Args:
            name(str): Name of the LabBook

        Returns:
            Labbook
        """
        # TODO: Lookup name based on logged in user when available
        id_data = {"username": get_logged_in_user(), "name": name, "owner": owner}
        return Labbook.create(id_data)

    def resolve_local_labbooks(self, args, context, info):
        """Method to return a all graphene LabbookSummary instances for the logged in user

        Uses the "currently logged in" user

        Returns:
            list(Labbook)
        """
        lb = LabBook()

        # TODO: Lookup name based on logged in user when available
        username = get_logged_in_user()
        labbooks = lb.list_local_labbooks(username=username)

        # Collect all labbooks for all owners
        edges = []
        for key in labbooks.keys():
            edges.extend(labbooks[key])
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, args)
        lbc.apply()

        # Get LabbookSummary instances
        id_data = {"username": username}
        edge_objs = []
        for edge, cursor in zip(lbc.edges, lbc.cursors):
            id_data["name"] = edge["name"]
            id_data["owner"] = edge["owner"]
            edge_objs.append(LabbookConnection.Edge(node=LabbookSummary.create(id_data), cursor=cursor))

        return LabbookConnection(edges=edge_objs, page_info=lbc.page_info)
