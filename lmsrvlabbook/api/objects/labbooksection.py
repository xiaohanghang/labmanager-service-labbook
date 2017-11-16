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
import graphene
import os
from lmcommon.logging import LMLogger
from lmcommon.labbook import LabBook

from lmsrvcore.auth.user import get_logged_in_username
from lmsrvcore.api import ObjectType
from lmsrvcore.api.connections import ListBasedConnection

from lmsrvlabbook.api.objects.labbookfile import LabbookFavorite, LabbookFile
from lmsrvlabbook.api.connections.labbookfileconnection import LabbookFileConnection, LabbookFavoriteConnection

logger = LMLogger.get_logger()


class LabbookSection(ObjectType):
    """A type representing a section within a LabBook (i.e., code, input, output
    """
    class Meta:
        interfaces = (graphene.relay.Node,)

    # List of files and directories, given a relative root directory within the section
    files = graphene.relay.ConnectionField(LabbookFileConnection, root=graphene.String())

    # List of all files and directories within the section
    all_files = graphene.relay.ConnectionField(LabbookFileConnection)

    # List of favorites for a given subdir (code, input, output)
    favorites = graphene.relay.ConnectionField(LabbookFavoriteConnection)

    @staticmethod
    def to_type_id(id_data):
        """Method to generate a single string that uniquely identifies this object

        Args:
            id_data(dict):

        Returns:
            str
        """
        return "{}&{}&{}".format(id_data["owner"], id_data["name"], id_data["section_name"])

    @staticmethod
    def parse_type_id(type_id):
        """Method to parse an ID for a given type into its identifiable variables returned as a dictionary of strings

        Args:
            type_id (str): type unique identifier

        Returns:
            dict
        """
        split = type_id.split("&")
        return {"owner": split[0], "name": split[1], "section_id": split[2]}

    @staticmethod
    def create(id_data):
        """Method to create a graphene LabBookSection object based on the node ID or owner+name+section

        id_data should at a minimum contain either `type_id` or `owner` & `name`

            {
                "type_id": <unique id for this object Type),
                "owner": <owner username (or org)>,
                "name": <name of the labbook>
            }

        Args:
            id_data(dict): A dictionary of variables that uniquely ID the instance. Can be a node ID or other vars

        Returns:
            Labbook
        """
        if "type_id" in id_data:
            id_data.update(LabbookSection.parse_type_id(id_data["type_id"]))
            del id_data["type_id"]

        if "username" not in id_data:
            id_data["username"] = get_logged_in_username()

        if "labbook_instance" not in id_data:
            lb = LabBook()
            lb.from_name(id_data["username"], id_data["owner"], id_data["name"])

        return LabbookSection(id=LabbookSection.to_type_id(id_data),
                              _id_data=id_data)

    def resolve_files(self, args, context, info):
        if "labbook_instance" not in self._id_data:
            lb = LabBook()
            lb.from_name(get_logged_in_username(), self._id_data['owner'], self._id_data['name'])
        else:
            lb = self._id_data["labbook_instance"]

        if args.get("root"):
            base_dir = os.path.join(self._id_data['section_name'], args.get("root")) + os.path.sep
        else:
            base_dir = self._id_data['section_name'] + os.path.sep
        base_dir = base_dir.replace(os.path.sep + os.path.sep, os.path.sep)

        # Get all files and directories, with the exception of anything in .git or .gigantum
        edges = lb.listdir(base_path=base_dir, show_hidden=False)
        # Generate naive cursors
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, args)
        lbc.apply()

        edge_objs = []
        try:
            for edge, cursor in zip(lbc.edges, lbc.cursors):
                id_data = {"user": get_logged_in_username(),
                           "owner": self._id_data['owner'],
                           "name": self._id_data['name'],
                           "file_info": edge}
                edge_objs.append(LabbookFileConnection.Edge(node=LabbookFile.create(id_data), cursor=cursor))

            return LabbookFileConnection(edges=edge_objs, page_info=lbc.page_info)
        except Exception as e:
            logger.exception(e)
            raise

    def resolve_all_files(self, args, context, info):
        if "labbook_instance" not in self._id_data:
            lb = LabBook()
            lb.from_name(get_logged_in_username(), self._id_data['owner'], self._id_data['name'])
        else:
            lb = self._id_data["labbook_instance"]

        # Get all files and directories, with the exception of anything in .git or .gigantum
        edges = lb.walkdir(base_path=self._id_data['section_name'], show_hidden=False)
        # Generate naive cursors
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, args)
        lbc.apply()

        edge_objs = []
        try:
            for edge, cursor in zip(lbc.edges, lbc.cursors):
                id_data = {"user": get_logged_in_username(),
                           "owner": self._id_data['owner'],
                           "name": self._id_data['name'],
                           "file_info": edge}
                edge_objs.append(LabbookFileConnection.Edge(node=LabbookFile.create(id_data), cursor=cursor))

            return LabbookFileConnection(edges=edge_objs, page_info=lbc.page_info)
        except Exception as e:
            logger.exception(e)
            raise

    def resolve_favorites(self, args, context, info):
        if "labbook_instance" not in self._id_data:
            lb = LabBook()
            lb.from_name(get_logged_in_username(), self._id_data['owner'], self._id_data['name'])
        else:
            lb = self._id_data["labbook_instance"]

        # Get all files and directories, with the exception of anything in .git or .gigantum
        edges = lb.get_favorites(self._id_data['section_name'])
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, args)
        lbc.apply()

        edge_objs = []
        try:
            for edge, cursor in zip(lbc.edges, lbc.cursors):
                id_data = {"user": get_logged_in_username(),
                           "owner": self._id_data['owner'],
                           "name": self._id_data['name'],
                           "subdir": self._id_data['section_name'],
                           "favorite_data": edge}
                edge_objs.append(LabbookFavoriteConnection.Edge(node=LabbookFavorite.create(id_data), cursor=cursor))

            return LabbookFavoriteConnection(edges=edge_objs, page_info=lbc.page_info)
        except Exception as e:
            logger.exception(e)
            raise
