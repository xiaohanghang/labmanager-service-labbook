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

from lmsrvcore.api.objects import Owner


class GitCommit(graphene.Interface):
    """An interface for any object that is represented by a git commit"""
    # The git commit hash
    hash = graphene.String()

    # The git commit hash, limited to 8-characters
    short_hash = graphene.String()

    # The datetime of the commit as an ISO-8601 encoded UTC datetime string
    committed_on = graphene.String()


class GitRef(graphene.Interface):
    """An interface for any git reference"""
    # The name of the reference
    name = graphene.String()

    # The prefix of the reference
    prefix = graphene.String()


class GitRepository(graphene.Interface):
    """An interface for Objects backended with git repositories (LabBook and Datasets)"""
    # The name of the underlying git repository.
    # Must be unique to what exists locally and unique in a user's library when pushing
    # Only A-Za-z0-9- allowed with no leading or trailing '-'
    namespace = graphene.String()

    # The name of the underlying git repository.
    # Must be unique to what exists locally and unique in a user's library when pushing
    # Only A-Za-z0-9- allowed with no leading or trailing '-'
    name = graphene.String()

    # A short description of the LabBook limited to 140 UTF-8 characters
    description = graphene.String()

    # Owner of the repository
    owner = graphene.Field(Owner)
