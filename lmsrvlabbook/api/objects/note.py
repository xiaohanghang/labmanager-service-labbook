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
from lmcommon.notes import NoteStore, NoteLogLevel

from lmsrvcore.auth.user import get_logged_in_user

from lmsrvcore.api import ObjectType
from lmsrvcore.api.connections import ListBasedConnection

from lmsrvlabbook.api.connections.noteobject import NoteObjectConnection
from lmsrvlabbook.api.objects.noteobject import NoteObject


# Expose NoteLogLevel enumeration as a graphene Enum
NoteLogLevelEnum = graphene.Enum.from_enum(NoteLogLevel)


class Note(ObjectType):
    """A type representing a single note entry in a labbook"""
    class Meta:
        interfaces = (graphene.relay.Node, )

    # The commit hash for this entry
    commit = graphene.ID()

    # The git commit hash this note references
    linked_commit = graphene.ID()

    # The git commit hash this note references
    note_detail_key = graphene.ID()

    # The short summary message of the note
    message = graphene.String()

    # TODO: update to User type once proper user model is implemented
    author = graphene.String()

    # The level of the note
    level = graphene.Field(NoteLogLevelEnum)

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
                "summary": <dict> If the summary has already been retrieved but not converted to a graphene object
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

        if "summary" not in id_data:
            # Shortcut to generate a graphene Note type if the not summary has already been pulled from the
            # gitlog using the NoteStore
            lb = LabBook()
            lb.from_name(id_data["username"], id_data["owner"], id_data["name"])

            # Create NoteStore instance
            note_db = NoteStore(lb)

            # get the record for the individual commit
            note = note_db.get_note_summary(id_data["commit"])
        else:
            note = id_data["summary"]

        return Note(id=Note.to_type_id(id_data),
                    commit=note['note_commit'],
                    linked_commit=note['linked_commit'],
                    note_detail_key=note['note_detail_key'],
                    level=note['level'].value,
                    timestamp=note['timestamp'],
                    author=note['author']['email'],
                    tags=note['tags'],
                    message=note['message'])

    def resolve_objects(self, args, context, info):
        """Method to populate the objects field

        Args:
            args:
            context:
            info:

        Returns:

        """
        if "objects" not in self.__dict__:
            # TODO: Use dataloader to access the detail object data as this implementation can have redundent IO
            id_data = self.parse_type_id(self.id)
            id_data["username"] = get_logged_in_user()
            lb = LabBook()
            lb.from_name(id_data["username"], id_data["owner"], id_data["name"])

            # Create NoteStore instance
            note_db = NoteStore(lb)

            # Get detailed record
            detail = note_db.get_detail_record(self.note_detail_key)
            edges = detail["objects"]

        else:
            edges = self.objects

        # Get all edges and cursors. Here, cursors are just an index into the refs
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, args)
        lbc.apply()

        # Get LabbookRef instances
        edge_objs = []
        for edge, cursor in zip(lbc.edges, lbc.cursors):
            id_data = self.parse_type_id(self.id)
            id_data.update({"note_detail_key": self.note_detail_key,
                            "note_object_key": edge.key})
            edge_objs.append(NoteObjectConnection.Edge(node=NoteObject.create(id_data), cursor=cursor))

        return NoteObjectConnection(edges=edge_objs,
                                    page_info=lbc.page_info)

    def resolve_free_text(self, args, context, info):
        """Method to page through branch Refs

        Args:
            args:
            context:
            info:

        Returns:

        """
        # If free_text has already been explicitly set move on
        if "free_text" not in self.__dict__:
            # TODO: Use dataloader to access the detail object data as this implementation can have redundent IO
            id_data = self.parse_type_id(self.id)
            id_data["username"] = get_logged_in_user()
            lb = LabBook()
            lb.from_name(id_data["username"], id_data["owner"], id_data["name"])

            # Create NoteStore instance
            note_db = NoteStore(lb)

            # Get detailed record
            detail = note_db.get_detail_record(self.note_detail_key)
            return detail["free_text"]

        else:
            return self.free_text
