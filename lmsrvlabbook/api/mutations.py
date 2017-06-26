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
import uuid
import os

import graphene
from .objects import Labbook
from .queries import _get_graphene_labbook

from lmcommon.labbook import LabBook
from lmcommon.api.util import get_logged_in_user
from lmcommon.api.objects import InputUser
from lmcommon.configuration import Configuration
from lmcommon.gitlib import get_git_interface


class CreateLabbook(graphene.Mutation):
    """Class for Mutator.  Don't use camel case in suffix, i.e. Labbook not LabBook """

    class Input:
        name = graphene.String()
        description = graphene.String()
        owner = graphene.Argument(InputUser)

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
               owner=args.get('owner'))

        # Get a graphene instance of the newly created LabBook
        new_labbook = _get_graphene_labbook(username, lb.name)
        return CreateLabbook(labbook=new_labbook)


class CreateBranch(graphene.Mutation):
    """Mutation create a NEW branch for a LabBook LOCALLY"""

    class Input:
        labbook_name = graphene.String()
        branch_name = graphene.String()

    # Return the LabBook instance
    labbook = graphene.Field(lambda: Labbook)

    @staticmethod
    def mutate(root, args, context, info):
        # TODO: Lookup name based on logged in user when available
        username = get_logged_in_user()

        # Load an existing LabBook
        labbook_obj = LabBook()
        labbook_obj.from_name(username, args.get('labbook_name'))

        # Create Branch
        git_obj = get_git_interface(Configuration().config["git"])
        git_obj.set_working_directory(os.path.join(git_obj.working_directory, username, labbook_obj.name))
        git_obj.create_branch(args.get('branch_name'))

        return CreateBranch(labbook=labbook_obj)


class CheckoutBranch(graphene.Mutation):
    """Mutation checkout an existing branch branch"""

    class Input:
        labbook_name = graphene.String()
        branch_name = graphene.String()

    # Return the LabBook instance
    labbook = graphene.Field(lambda: Labbook)

    @staticmethod
    def mutate(root, args, context, info):
        # TODO: Lookup name based on logged in user when available
        username = get_logged_in_user()

        # Load an existing LabBook
        labbook_obj = LabBook()
        labbook_obj.from_name(username, args.get('labbook_name'))

        # Checkout Branch
        git_obj = get_git_interface(Configuration().config["git"])
        git_obj.set_working_directory(os.path.join(git_obj.working_directory, username, labbook_obj.name))
        git_obj.fetch()
        git_obj.checkout(args.get('branch_name'))

        return CheckoutBranch(labbook=labbook_obj)


class LabbookMutations(graphene.ObjectType):
    """Entry point for all graphql mutations"""
    create_labbook = CreateLabbook.Field()
    create_branch = CreateBranch.Field()
    checkout_branch = CheckoutBranch.Field()
