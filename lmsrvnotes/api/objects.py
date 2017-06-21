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
from graphene.types import datetime
from graphene.types import json


class NoteSummary (graphene.ObjectType):
    """The brief version of a note derived from the git log"""
    lbname = graphene.String()
    id = graphene.ID()
    message = graphene.String()
    loglevel = graphene.String()
    tags = graphene.List(graphene.String)
    timestamp = datetime.DateTime()


# RBTODO duplicated fields -- hieararchy? interface?

class Note(graphene.ObjectType):
    """The long version of a note stored in the notes files"""

    lbname = graphene.String()
    id = graphene.ID()
    message = graphene.String()
    loglevel = graphene.String()
    tags = graphene.List(graphene.String)
    timestamp = datetime.DateTime()

    # longer fields
    freetext = graphene.String()

    # kvobject are a json dumps of whatever
    kvobjects = json.JSONString()


class Notes (graphene.ObjectType):
    """The summary of notes for a labbook"""

    # the unique name of a LabBook
    lbname = graphene.String()

    # summary entries
    entries = graphene.List(NoteSummary)

    # The username of the owner - To be replaced with a proper User interface
    username = graphene.String()

