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
import os

import graphene
from graphene import resolve_only_args

from lmcommon.configuration import Configuration
from lmcommon.gitlib import get_git_interface
from lmcommon.labbook import LabBook

from lmsrvcore.api.objects import Owner
from lmsrvcore.auth.user import get_logged_in_user

from lmsrvlabbook.api.objects import Labbook, LabbookRef, LabbookCommit


class LabbookQuery(graphene.AbstractType):
    """Entry point for all LabBook queryable fields"""
    # Node Fields for Relay
    node = graphene.relay.Node.Field()

    labbook = graphene.Field(Labbook, owner=graphene.String(), name=graphene.String())
    #labbooks = graphene.Field(graphene.List(Labbook))
    #users = graphene.Field(graphene.List(User))

    # TODO: Double check if the decorator is needed
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

    #@resolve_only_args
    #def resolve_labbooks(self):
    #    """Method to return a all graphene Labbook instances for the logged in user
#
    #    Uses the "currently logged in" user
#
    #    Returns:
    #        list(Labbook)
    #    """
    #    lb = LabBook()
#
    #    # TODO: Lookup name based on logged in user when available
    #    username = get_logged_in_user()
    #    labbooks = lb.list_local_labbooks(username=username)
#
    #    result = []
    #    if username in labbooks:
    #        for lb_name in labbooks[username]:
    #            result.append(_get_graphene_labbook(username, lb_name))
    #    else:
    #        raise ValueError("User {} not found.".format(username))
#
    #    return result
#
    #@resolve_only_args
    #def resolve_users(self):
    #    """Method to return a list of users who have logged into the LabManager instance
#
    #    Returns:
    #        list(str)
    #    """
    #    lb = LabBook()
#
    #    labbooks = lb.list_local_labbooks()
#
    #    result = []
    #    for user in labbooks.keys():
    #        result.append(User(username=user))
#
    #    return result


