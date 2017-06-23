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


# @DK do we want an enum,  or just use text.
class LogLevel(graphene.Enum):
    USER_MAJOR = 11
    USER_MINOR = 12
    AUTO_MAJOR = 21
    AUTO_MINOR = 22
    AUTO_DETAIL = 23
    

class NoteSummary(graphene.ObjectType):
    """The brief version of a note derived from the git log"""
    lbname = graphene.String()
    commit = graphene.ID()
    linkedcommit = graphene.ID()
    author = graphene.String()
    message = graphene.String()
    level = graphene.String()
    tags = graphene.List(graphene.String)
    timestamp = datetime.DateTime()


class Notes(graphene.ObjectType):
    """The summary of notes for a labbook"""

    # the unique name of a LabBook
    lbname = graphene.String()

    # summary entries
    entries = graphene.List(NoteSummary)


class NoteObjectAbs(graphene.AbstractType):
    """Container for arbitrary objects
        * keys are strings.
        * object type the content
        * values are uninterpreted blobs encoded as strings
    """
    key = graphene.String()
    objecttype = graphene.String()      # TODO make an ENUM?
    value = graphene.String()


# Input and output types needed for requests and mutations
class NoteObjectIn(graphene.InputObjectType, NoteObjectAbs):
    pass


class NoteObject(graphene.ObjectType, NoteObjectAbs):
    pass


class Note(graphene.ObjectType):
    """The long version of a note that included details"""

    # TODO inheritance from NoteSummary didn't work here.
    # Summary fields in git commit log
    lbname = graphene.String()
    commit = graphene.ID()
    linkedcommit = graphene.ID()
    author = graphene.String()
    message = graphene.String()
    level = graphene.String()
    tags = graphene.List(graphene.String)
    timestamp = datetime.DateTime()

    # detail fields in NoteStore
    freetext = graphene.String()
    objects = graphene.List(NoteObject)


