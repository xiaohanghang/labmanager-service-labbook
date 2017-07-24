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
import json
import graphene
import base64
import re
from graphene.types import datetime

from lmcommon.labbook import LabBook
from lmcommon.notes import NoteStore

from lmsrvcore.auth.user import get_logged_in_user

from lmsrvcore.api import ObjectType
from lmsrvcore.api.connections import ListBasedConnection

from lmsrvlabbook.api.connections.noteobject import NoteObjectConnection


class LogLevel(graphene.Enum):
    """Enumeration representing the note 'level' in the hierarchy"""
    # User generated Notes
    USER_MAJOR = 11
    USER_MINOR = 12

    # Automatic "system" generated notes
    AUTO_MAJOR = 21
    AUTO_MINOR = 22
    AUTO_DETAIL = 23


class Note(ObjectType):
    """A type representing a single note entry in a labbook"""
    class Meta:
        interfaces = (graphene.relay.Node, )

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

    # Detailed information
    free_text = graphene.String()

    # Connection to Note Blob Objects
    objects = graphene.relay.ConnectionField(NoteObjectConnection)

    @staticmethod
    def to_type_id(id_data):
        """Method to generate a single string that uniquely identifies this object

        Args:
            id_data(dict):

        Returns:
            str
        """
        return "{}&{}&{}".format(id_data["owner"], id_data["name"], id_data["commit"])


    @staticmethod
    def parse_type_id(type_id):
        """Method to parse an ID for a given type into its identifiable variables returned as a dictionary of strings

        Args:
            type_id (str): type unique identifier

        Returns:
            dict
        """
        split = type_id.split("&")
        return {"owner": split[0], "name": split[1], "commit": split[2]}

    @staticmethod
    def create(id_data):
        """Method to create a graphene Note object based on the node ID or owner+name

        id_data should at a minimum contain either `type_id` or `owner` & `name`

            {
                "type_id": <unique id for this object Type),
                "owner": <owner username (or org)>,
                "name": <name of the labbook>
            }

        Args:
            id_data(dict): A dictionary of variables that uniquely ID the instance. Can be a node ID or other vars

        Returns:
            Note
        """
        if "type_id" in id_data:
            id_data.update(Note.parse_type_id(id_data["type_id"]))
            del id_data["type_id"]

        if "username" not in id_data:
            id_data["username"] = get_logged_in_user()

        lb = LabBook()
        lb.from_name(id_data["username"], id_data["owner"], id_data["name"])

        # Create NoteStore instance
        note_db = NoteStore(lb)

        # get the record for the individual commit
        entry = lb.log_entry(commit=id_data["commit"])

        # filter log on Notes
        regex = r"gtmNOTE_: ([\w\s\S]+)\ngtmjson_metadata_: (.*)"

        m = re.match(regex, entry['message'])
        if m:
            # summary data from git log
            message = m.group(1)
            note_metadata = json.loads(m.group(2))

            # get the detail from notes storage.
            note_detail = note_db.get_entry(note_metadata["linked_commit"])
        else:
            raise ValueError("Commit {} not found".format(id_data["commit"]))

        return Note(id=Note.to_type_id(id_data),
                    commit=entry['commit'],
                    linked_commit=note_metadata['linked_commit'],
                    level=note_metadata['level'],
                    timestamp=entry['committed_on'],
                    author=entry['author'],
                    tags=note_metadata['tags'],
                    message=message,
                    free_text=note_detail['free_text'])#,
                    #_note_detail=note_detail,
                    #_owner=id_data["owner"],
                    #_labbook_name=id_data["name"])

    def resolve_objects(self, args, context, info):
        """Method to page through branch Refs

        Args:
            args:
            context:
            info:

        Returns:

        """
        # TODO: Design a better cursor implementation that doesn't need to load everything to page on each request
        # Get all edges and cursors. Here, cursors are just an index into the refs
        edges = [x for x in self.note_detail]
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, args)
        lbc.apply()

        # Get LabbookRef instances
        edge_objs = []
        for edge, cursor in zip(lbc.edges, lbc.cursors):
            id_data = {"owner": self._owner,
                       "name": self._labbook_name,
                       "linked_commit": self.linked_commit,
                       "note_object_key": edge.key}
            edge_objs.append(NoteObjectConnection.Edge(node=Note.create(id_data), cursor=cursor))

        return NoteObjectConnection(edges=edge_objs,
                                    page_info=lbc.page_info)

