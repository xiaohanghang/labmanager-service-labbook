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
from graphene import resolve_only_args

from .objects import Labbook, User

from lmcommon.labbook import LabBook


class LabbookQueries(graphene.ObjectType):
    """Entry point for all LabBook queries"""
    labbook = graphene.Field(Labbook, name=graphene.String())
    labbooks = graphene.Field(graphene.List(Labbook))
    users = graphene.Field(graphene.List(User))

    # TODO: @randal - what is resolve only args?
    @resolve_only_args
    def resolve_labbook(self, name):
        lb = LabBook()

        # TODO: Lookup name based on logged in user when available
        username = "default"
        lb.from_name(username, name)

        return Labbook(name=lb.name, id=lb.id, description=lb.description, username=lb.username)

    @resolve_only_args
    def resolve_labbooks(self):
        lb = LabBook()

        # TODO: Lookup name based on logged in user when available
        username = "default"
        labbooks = lb.list_local_labbooks(username=username)

        result = []
        if username in labbooks:
            for lb_name in labbooks[username]:
                lb = LabBook()
                lb.from_name(username, lb_name)
                result.append(Labbook(name=lb.name, id=lb.id, description=lb.description, username=lb.username))
        else:
            raise ValueError("User {} not found.".format(username))

        return result

    @resolve_only_args
    def resolve_users(self):
        lb = LabBook()

        # TODO: Lookup name based on logged in user
        labbooks = lb.list_local_labbooks()

        result = []
        for user in labbooks.keys():
            result.append(User(username=user))

        return result


