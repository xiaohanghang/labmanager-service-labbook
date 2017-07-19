
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

from lmcommon.gitlib import get_git_interface
from lmcommon.configuration import Configuration
from lmcommon.labbook import LabBook

from lmsrvcore.auth.user import get_logged_in_user

from lmsrvlabbook.api.objects.ref import LabbookRef
from lmsrvlabbook.api.objects.labbook import Labbook


class CreateBranch(graphene.relay.ClientIDMutation):
    """Mutation create a NEW branch for a LabBook LOCALLY"""
    class Input:
        owner = graphene.String()
        labbook_name = graphene.String(required=True)
        branch_name = graphene.String(required=True)

    # Return the LabBook instance
    branch = graphene.Field(LabbookRef)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        """Method to perform mutation
        Args:
            input:
            context:
            info:
        Returns:
        """
        username = get_logged_in_user()
        if not input.get("owner"):
            owner = get_logged_in_user()
        else:
            owner = input.get("owner")

        # Load an existing LabBook
        labbook_obj = LabBook()
        labbook_obj.from_name(username, owner, input.get('labbook_name'))

        # Create Branch
        labbook_obj.git.create_branch(input.get("branch_name"))

        # Create a LabbookRef to the branch
        id_data = {"username": username,
                   "owner": owner,
                   "name": input.get("labbook_name"),
                   "prefix": None,
                   "branch": input.get("branch_name"),
                   "git": labbook_obj.git
                   }
        return CreateBranch(branch=LabbookRef.create(id_data))


class CheckoutBranch(graphene.relay.ClientIDMutation):
    """Mutation checkout an existing branch branch"""
    class Input:
        owner = graphene.String()
        labbook_name = graphene.String(required=True)
        branch_name = graphene.String(required=True)

    # Return the LabBook instance
    labbook = graphene.Field(lambda: Labbook)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        """Method to perform mutation
        Args:
            input:
            context:
            info:
        Returns:
        """
        username = get_logged_in_user()
        if not input.get("owner"):
            owner = get_logged_in_user()
        else:
            owner = input.get("owner")

        # Load an existing LabBook
        labbook_obj = LabBook()
        labbook_obj.from_name(username, owner, input.get('labbook_name'))

        # Checkout
        labbook_obj.git.fetch()
        labbook_obj.git.checkout(input.get('branch_name'))

        # Create a LabbookRef to the branch
        id_data = {"username": username,
                   "owner": owner,
                   "name": input.get("labbook_name"),
                   "prefix": None,
                   "branch": labbook_obj.git.get_current_branch_name(),
                   "git": labbook_obj.git
                   }
        return CheckoutBranch(labbook=Labbook.create(id_data))

