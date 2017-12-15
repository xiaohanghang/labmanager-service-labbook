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
import os

import graphene
from graphene.types import datetime

from lmcommon.labbook import LabBook
from lmsrvcore.auth.user import get_logged_in_username
from lmsrvcore.api import ObjectType, logged_query


class LabbookFile(ObjectType):
    """A type representing a file or directory inside the labbook file system."""

    class Meta:
        interfaces = (graphene.relay.Node,)

    # True indicates that path points to a directory
    is_dir = graphene.Boolean()

    # True indicates that path points to a favorite
    is_favorite = graphene.Boolean()

    # Modified at contains timestamp of last modified - NOT creation in epoch time.
    modified_at = graphene.Int()

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
        return f"{id_data['owner']}&{id_data['name']}&{id_data['section']}&{id_data['key']}"

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
        return {'owner': tokens[0],
                'name': tokens[1],
                'section': tokens[2],
                'key': tokens[3]}

    @staticmethod
    @logged_query
    def create(id_data):

        if "type_id" in id_data:
            # Loading as node so need to populate file data
            id_data = LabbookFile.parse_type_id(id_data['type_id'])

            # Force to logged in user always
            id_data["username"] = get_logged_in_username()

            lb = LabBook()
            lb.from_name(id_data["username"], id_data["owner"], id_data["name"])

            # Create data to populate edge
            id_data['file_info'] = lb.get_file_info(id_data["section"], id_data['key'])

        else:
            # Loading from a query, so you have the file data already
            if "username" not in id_data:
                id_data["username"] = get_logged_in_username()

        # Set key in id data if missing so to_type_id() works.
        id_data['key'] = id_data['file_info']['key']

        return LabbookFile(id=LabbookFile.to_type_id(id_data),
                           is_dir=id_data['file_info']['is_dir'],
                           modified_at=round(id_data['file_info']['modified_at']),
                           key=id_data['file_info']['key'],
                           size=id_data['file_info']['size'],
                           is_favorite=id_data['file_info']['is_favorite'])


class LabbookFavorite(ObjectType):
    """A type representing a file or directory that has been favorited in the labbook file system."""

    class Meta:
        interfaces = (graphene.relay.Node,)

    # Index value indicating the order of the favorite
    index = graphene.Int()

    # Relative path from labbook root directory.
    key = graphene.String()

    # Short description about the favorite
    description = graphene.String()

    # True indicates that the favorite is a directory
    is_dir = graphene.Boolean()

    @staticmethod
    def to_type_id(id_data):
        """Method to generate a single string that uniquely identifies this object

        Args:
            id_data(dict):

        Returns:
            str
        """
        return f"{id_data['owner']}&{id_data['name']}&{id_data['section']}&{id_data['index']}"

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
        return {'owner': tokens[0],
                'name': tokens[1],
                'section': tokens[2],
                'index': tokens[3]}

    @staticmethod
    @logged_query
    def create(id_data):

        if 'favorite_data' in id_data:
            item = id_data['favorite_data']

            # Set id data so ID will auto-generate. Need to clean this up in the future so not so complex for developer
            id_data['index'] = item['index']
        else:
            if "type_id" in id_data:
                id_data = LabbookFavorite.parse_type_id(id_data['type_id'])

            if "username" not in id_data:
                id_data["username"] = get_logged_in_username()

            lb = LabBook()
            lb.from_name(id_data["username"], id_data["owner"], id_data["name"])
            data = lb.get_favorites(id_data['section'])

            # Make sure index is valid
            if int(id_data["index"]) > len(data) - 1:
                raise ValueError("Invalid favorite index value")
            if int(id_data["index"]) < 0:
                raise ValueError("Invalid favorite index value")

            # Pull out single entry
            item = data[int(id_data['index'])]

        return LabbookFavorite(id=LabbookFavorite.to_type_id(id_data),
                               index=item["index"],
                               key=item['key'],
                               description=item['description'],
                               is_dir=item['is_dir'])
