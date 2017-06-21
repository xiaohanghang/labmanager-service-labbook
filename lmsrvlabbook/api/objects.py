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


class Labbook(graphene.ObjectType):
    """The LabBook type that represents a LabBook instance on disk"""
    # A unique identifier for the LabBook
    id = graphene.ID()

    # The name of the LabBook. Must be unique to what exists locally and unique in a user's library when pushing
    # Only A-Za-z0-9- allowed
    name = graphene.String()

    # A short description of the LabBook limited to 140 UTF-8 characters
    description = graphene.String()

    # The username of the owner - To be replaced with a proper User interface
    username = graphene.String()

    # The name of the current branch
    branch = graphene.String()

    # The git commit hash currently checked out
    commit = graphene.String()

    # The git commit hash currently checked out limited to 8 characters
    commit_short = graphene.String()


class User(graphene.ObjectType):
    """The User type represents a user logged into the LabManager"""
    username = graphene.String()
