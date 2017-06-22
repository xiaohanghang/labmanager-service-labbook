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

from .objects import Labbook, LabbookRef, LabbookCommit

from lmcommon.labbook import LabBook
from lmcommon.gitlib import get_git_interface
from lmcommon.configuration import Configuration
from lmcommon.api.objects import User
from lmcommon.api.util import get_logged_in_user


def _get_graphene_labbook(username, labbook_name):
    """ Private method to get a Graphene Labbook object from disk based on the username and LabBook name

    Args:
        username(str): Username of the "logged in" user
        labbook_name(str): Name of the LabBook to load

    Returns:
        Labbook
    """
    lb = LabBook()
    lb.from_name(username, labbook_name)

    # Get the git information
    git = get_git_interface(Configuration().config["git"])
    git.set_working_directory(os.path.join(git.working_directory, username, labbook_name))

    # Get branches
    branch_listing = git.list_branches()

    return Labbook(name=lb.name, id=lb.id, description=lb.description, owner=User(username=lb.owner["username"]),
                   commit=_get_graphene_labbook_commit(lb),
                   local_branches=branch_listing["local"], remote_branches=branch_listing["remote"],
                   active_branch=_get_graphene_labbook_ref(lb, git_obj=git))


def _get_graphene_labbook_commit(labbook_obj):
    """ Private method to get a Graphene LabbookCommit object from a LabBook instance

    Args:
        labbook_obj(LabBook): A lmcommon.labbook.LabBook instance

    Returns:
        LabbookCommit
    """
    # TODO: Lookup name based on logged in user when available
    username = get_logged_in_user()

    # Get the commit information
    git = get_git_interface(Configuration().config["git"])
    git.set_working_directory(os.path.join(git.working_directory, username, labbook_obj.name))

    return LabbookCommit(hash=git.commit_hash, short_hash=git.commit_hash_short,
                         committed_on=git.committed_on.isoformat())


def _get_graphene_labbook_ref(labbook_obj, git_obj=None):
    """ Private method to get a Graphene LabbookRef object from a LabBook instance

    Args:
        labbook_obj(LabBook): A lmcommon.labbook.LabBook instance
        git_obj(lmcommon.gitlib.GitRepoInterface): Optional initialized git repo instance

    Returns:
        LabbookCommit
    """
    if not git_obj:
        # TODO: Lookup name based on logged in user when available
        username = get_logged_in_user()

        # Get the git information
        git_obj = get_git_interface(Configuration().config["git"])
        git_obj.set_working_directory(os.path.join(git_obj.working_directory, username, labbook_obj.name))

    return LabbookRef(commit=_get_graphene_labbook_commit(labbook_obj),
                      name=git_obj.get_current_branch_name(), prefix=git_obj.git_path.rsplit("/", 1)[0])


class LabbookQueries(graphene.ObjectType):
    """Entry point for all LabBook queries"""
    labbook = graphene.Field(Labbook, name=graphene.String())
    labbooks = graphene.Field(graphene.List(Labbook))
    users = graphene.Field(graphene.List(User))

    # TODO: Double check if the decorator is needed
    @resolve_only_args
    def resolve_labbook(self, name):
        """Method to return a graphene Labbok instance based on the name

        Uses the "currently logged in" user

        Args:
            name(str): Name of the LabBook

        Returns:
            Labbook
        """
        # TODO: Lookup name based on logged in user when available
        username = get_logged_in_user()
        return _get_graphene_labbook(username, name)

    @resolve_only_args
    def resolve_labbooks(self):
        """Method to return a all graphene Labbook instances for the logged in user

        Uses the "currently logged in" user

        Returns:
            list(Labbook)
        """
        lb = LabBook()

        # TODO: Lookup name based on logged in user when available
        username = get_logged_in_user()
        labbooks = lb.list_local_labbooks(username=username)

        result = []
        if username in labbooks:
            for lb_name in labbooks[username]:
                result.append(_get_graphene_labbook(username, lb_name))
        else:
            raise ValueError("User {} not found.".format(username))

        return result

    @resolve_only_args
    def resolve_users(self):
        """Method to return a list of users who have logged into the LabManager instance

        Returns:
            list(str)
        """
        lb = LabBook()

        # TODO: Lookup name based on logged in user
        labbooks = lb.list_local_labbooks()

        result = []
        for user in labbooks.keys():
            result.append(User(username=user))

        return result


