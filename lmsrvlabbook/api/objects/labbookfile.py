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
import base64
import datetime
import json

import graphene
from graphene.types import datetime

from lmcommon.labbook import LabBook
from lmsrvcore.auth.user import get_logged_in_user
from lmsrvcore.api import ObjectType


class LabbookFile(ObjectType):
    """A type representing a file or directory inside the labbook file system."""

    class Meta:
        interfaces = (graphene.relay.Node,)

    # True indicates that path points to a directory
    is_dir = graphene.Boolean()

    # Modified at contains timestmap of last modified - NOT creation.
    modified_at = datetime.DateTime()

    # Relative path from labbook root directory.
    key = graphene.String()

    # Size in bytes.
    size = graphene.Int()

    @staticmethod
    def to_type_id(id_data):
        """Method to generate a single string that uniquely identifies this object

        Args:
            id_data(dict):

        Returns:
            str
        """
        return f"{id_data['user']}&{id_data['owner']}&{id_data['name']}&{id_data['enc_file_data']}"

    @staticmethod
    def parse_type_id(type_id):
        """Method to parse an ID for a given type into its identifiable variables returned as a dictionary of strings

        Args:
            type_id (str): type unique identifier

        Returns:
            dict
        """
        tokens = type_id.split('&')
        assert len(tokens) == 4, "type_id for LabbookFile should have 4 tokens"
        return {'user': tokens[0],
                'owner': tokens[1],
                'name': tokens[2],
                'enc_file_data': tokens[3].decode()}

    @staticmethod
    def create(id_data):
        if "username" not in id_data:
            id_data["username"] = get_logged_in_user()

        lb = LabBook()
        lb.from_name(id_data["username"], id_data["owner"], id_data["name"])

        dec_file_data = base64.b64decode(id_data['enc_file_data'])
        file_info = json.loads(dec_file_data)
        parsed_date = datetime.datetime.datetime.utcfromtimestamp(int(file_info['modified_at']))

        return LabbookFile(is_dir=file_info['is_dir'],
                           modified_at=parsed_date,
                           key=file_info['key'],
                           size=file_info['size'])
