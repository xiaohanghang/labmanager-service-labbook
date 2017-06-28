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


class LogLevel(graphene.Enum):
    """Enumeration representing the note 'level' in the hierarchy"""
    # User generated Notes
    USER_MAJOR = 11
    USER_MINOR = 12

    # Automatic "system" generated notes
    AUTO_MAJOR = 21
    AUTO_MINOR = 22
    AUTO_DETAIL = 23
    

class NoteSummaryType(graphene.AbstractType):
    """The brief version of a note derived from the git log"""
    # The name of the LabBook that contains this note
    labbook_name = graphene.String()

    # The commit hash for this entry
    commit = graphene.ID()

    # The git commit hash this note references
    linked_commit = graphene.ID()

    # The short summary message of the note
    message = graphene.String()

    # TODO: update to User type once proper user model is implemented
    author = graphene.String()

    # The level of the note
    level = graphene.Field(LogLevel)

    # Tags for the note
    tags = graphene.List(graphene.String)

    # Datetime of the note
    timestamp = datetime.DateTime()


class NoteObjectType(graphene.AbstractType):
    """Container for arbitrary objects stored within a note"""
    # Name of the object
    key = graphene.String()

    # Content type of the object
    # TODO make an ENUM
    object_type = graphene.String()

    # Uninterpreted blobs encoded as string
    value = graphene.String()


# Input and output types needed for requests and mutations
class NoteObjectInput(graphene.InputObjectType, NoteObjectType):
    pass


class NoteObject(graphene.ObjectType, NoteObjectType):
    pass


class NoteSummary(graphene.ObjectType, NoteSummaryType):
    pass


class Notes(graphene.ObjectType):
    """The summary of notes for a labbook"""

    # The name of the LabBook that contains this note
    labbook_name = graphene.String()

    # List of summaries
    # TODO: update to a connection for pagination support
    entries = graphene.List(NoteSummary)


class Note(graphene.ObjectType, NoteSummaryType):
    """The long version of a note that included details stored outside the git log"""
    # Detail fields in NoteStore
    free_text = graphene.String()
    objects = graphene.List(NoteObject)


