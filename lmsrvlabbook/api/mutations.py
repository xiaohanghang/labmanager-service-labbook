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

import graphene
from .objects import Labbook

from lmcommon.labbook import LabBook


class CreateLabbook(graphene.Mutation):
    """Class for Mutator.  Don't use camel case in suffix, i.e. Labbook not LabBook """

    class Input:
        name = graphene.String()
        description = graphene.String()

    # Return the LabBook instance
    labbook = graphene.Field(lambda: Labbook)

    @staticmethod
    def mutate(root, args, context, info):
        # Create a new empty LabBook
        lb = LabBook()
        lb.new(username="default",
               name=args.get('name'),
               description=args.get('description'))

        labbook = Labbook(name=lb.name, id=lb.id, description=lb.description, username=lb.username)
        return CreateLabbook(labbook=labbook)


class CreateLabbookBranch(graphene.Mutation):
    """Create a new Branch in an existing LabBook"""

    class Input:
        name = graphene.String()

    # Return the LabBook instance
    labbook = graphene.Field(lambda: Labbook)

    @staticmethod
    def mutate(root, args, context, info):
        # Create a new empty LabBook
        lb = LabBook()
        lb.new(username="default",
               name=args.get('name'),
               description=args.get('description'))

        labbook = Labbook(name=lb.name, id=lb.id, description=lb.description, username=lb.username)
        return CreateLabbook(labbook=labbook)


class LabbookMutations(graphene.ObjectType):
    """Entry point for all graphql mutations"""
    create_labbook = CreateLabbook.Field()
