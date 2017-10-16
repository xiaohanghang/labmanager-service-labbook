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

from lmcommon.labbook import LabBook
from lmcommon.notes import NoteStore

from lmsrvcore.auth.user import get_logged_in_user

from lmsrvcore.api import ObjectType


class NoteObjectType(graphene.AbstractType):
    """Container for arbitrary objects stored within a note"""

    class Meta:
        interfaces = (graphene.relay.Node,)

    # Name of the object
    key = graphene.String()

    # Content type of the object
    # TODO make an ENUM
    type = graphene.String()

    # Uninterpreted blobs encoded as string
    value = graphene.String()


class NoteObject(ObjectType, NoteObjectType):
    """Container for arbitrary objects stored within a note"""

    class Meta:
        interfaces = (graphene.relay.Node,)

    @staticmethod
    def to_type_id(id_data):
        """Method to generate a single string that uniquely identifies this object

        Args:
            id_data(dict):

        Returns:
            str
        """
        return "{}&{}&{}&{}".format(id_data["owner"], id_data["name"], id_data["note_detail_key"],
                                    id_data["note_object_key"])

    @staticmethod
    def parse_type_id(type_id):
        """Method to parse an ID for a given type into its identifiable variables returned as a dictionary of strings

        Args:
            type_id (str): type unique identifier

        Returns:
            dict
        """
        split = type_id.split("&")
        return {"owner": split[0], "name": split[1], "note_detail_key": split[2], "note_object_key": split[3]}

    @staticmethod
    def create(id_data):
        """Method to create a graphene NoteObject object based on the node ID or owner+name+note_object_key

            {
                "type_id": <unique id for this object Type),
                "username": <optional logged in user>,
                "owner": <owner username (or org)>,
                "name": <name of the labbook>
                "note_object_key": <key for the object to retrieve>
                "note_detail_record": <optional dict of note detail data from the `get_detail_record()` method
            }

        Args:
            id_data(dict): A dictionary of variables that uniquely ID the instance. Can be a node ID or other vars

        Returns:
            NoteObject
        """
        if "type_id" in id_data:
            id_data.update(NoteObject.parse_type_id(id_data["type_id"]))
            del id_data["type_id"]

        if "username" not in id_data:
            id_data["username"] = get_logged_in_user()

        lb = LabBook()
        lb.from_name(id_data["username"], id_data["owner"], id_data["name"])

        # Create NoteStore instance
        note_db = NoteStore(lb)

        if "note_detail_record" not in id_data:
            # get the detail record from notes storage.
            note_detail = note_db.get_detail_record(id_data["note_detail_key"])
        else:
            note_detail = id_data["note_detail_record"]

        for obj in note_detail['objects']:
            if obj.key == id_data["note_object_key"]:
                return NoteObject(id=NoteObject.to_type_id(id_data),
                                  key=obj.key,
                                  type=obj.type,
                                  value=obj.value)

        # If you are here, key not found
        return []


# Input and output types needed for requests and mutations
class NoteObjectInput(graphene.InputObjectType, NoteObjectType):
    pass
