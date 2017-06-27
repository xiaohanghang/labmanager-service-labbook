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

from lmcommon.api.interfaces import GitObject, RefObject, RepositoryObjectDetails, Node


class LabbookCommit(graphene.ObjectType):
    """An object representing a commit to a LabBook"""
    class Meta:
        interfaces = (GitObject, )


class LabbookRef(graphene.ObjectType):
    """An object representing a git reference in a LabBook repository"""
    class Meta:
        interfaces = (RefObject, )

    # The target commit the reference points to
    commit = graphene.Field(LabbookCommit)


class Labbook(graphene.ObjectType):
    """The LabBook type that represents a LabBook instance on disk"""
    class Meta:
        interfaces = (Node, RepositoryObjectDetails)

    # The name of the current branch
    active_branch = graphene.Field(LabbookRef)

    # List of available local branches
    local_branches = graphene.List(graphene.String)

    # List of available remote branches
    remote_branches = graphene.List(graphene.String)

    # The git commit of the currently checked out branch
    commit = graphene.Field(LabbookCommit)

