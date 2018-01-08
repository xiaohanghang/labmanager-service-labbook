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
from lmsrvcore.api import ObjectType, logged_query
from lmsrvcore.api.connections import ListBasedConnection

from lmsrvlabbook.api.objects.labbookfile import LabbookFavorite, LabbookFile
from lmsrvlabbook.api.connections.labbookfileconnection import LabbookFileConnection, LabbookFavoriteConnection
from lmsrvlabbook.dataloader.labbook import LabBookLoader

logger = LMLogger.get_logger()


class LabbookSection(ObjectType,  interfaces=(graphene.relay.Node,)):
    """A type representing a section within a LabBook (i.e., code, input, output)
    """
    # Section name (code, input, output)
    section = graphene.String()

    # List of files and directories, given a relative root directory within the section
    files = graphene.relay.ConnectionField(LabbookFileConnection, root=graphene.String())

    # List of all files and directories within the section
    all_files = graphene.relay.ConnectionField(LabbookFileConnection)

    # List of favorites for a given subdir (code, input, output)
    favorites = graphene.relay.ConnectionField(LabbookFavoriteConnection)

    @staticmethod
    def to_type_id(owner_name: str, labbook_name: str, section: str):
        """Method to generate a single string that uniquely identifies this object

        Args:
            owner_name(str): username or org name that owns the labbook
            labbook_name(str): name of the labbook
            section(str): name of the section

        Returns:
            str
        """
        return "{}&{}&{}".format(owner_name, labbook_name, section)

    @staticmethod
    def parse_type_id(type_id):
        """Method to parse an ID for a given type into its identifiable variables returned as a dictionary of strings

        Args:
            type_id (str): type unique identifier

        Returns:
            dict
        """
        split = type_id.split("&")
        return {"owner_name": split[0], "labbook_name": split[1], "section": split[2]}

    @staticmethod
    @logged_query
    def create(owner_name: str, labbook_name: str, section: str, labbook_loader: LabBookLoader):
        """Method to create a graphene LabBookSection object

        Args:
            owner_name(str): username or org name that owns the labbook
            labbook_name(str): name of the labbook
            section(str): name of the section
            labbook_loader(LabBookLoader): a LabBookLoader dataloader instance

        Returns:
            Labbook
        """
        return LabbookSection(id=LabbookSection.to_type_id(owner_name, labbook_name, section),
                              _loader=labbook_loader)

    def resolve_files(self, info):
        """Resolver for getting file listing in a single directory"""
        lb = self._loader.load(f"{get_logged_in_username()}&{self.owner.username}&{self.name}").get()

        #TODO: REFACTOR what is this?
        base_dir = None
        if info.context.get("root"):
            base_dir = info.context.get("root") + os.path.sep
            base_dir = base_dir.replace(os.path.sep + os.path.sep, os.path.sep)

        # Get all files and directories, with the exception of anything in .git or .gigantum
        edges = lb.listdir(self.section, base_path=base_dir, show_hidden=False)

        # Generate naive cursors
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, info.context)
        lbc.apply()

        edge_objs = []
        try:
            for edge, cursor in zip(lbc.edges, lbc.cursors):
                id_data = {"user": get_logged_in_username(),
                           "owner": self._id_data['owner'],
                           "section": self._id_data['section'],
                           "name": self._id_data['name'],
                           "file_info": edge}
                edge_objs.append(LabbookFileConnection.Edge(node=LabbookFile.create(**id_data), cursor=cursor))

            return LabbookFileConnection(edges=edge_objs, page_info=lbc.page_info)
        except Exception as e:
            logger.exception(e)
            raise

    def resolve_all_files(self, info, args):
        """Resolver for getting all files in a LabBook section"""
        if "labbook_instance" not in self._id_data:
            lb = LabBook()
            lb.from_name(get_logged_in_username(), self._id_data['owner'], self._id_data['name'])
        else:
            lb = self._id_data["labbook_instance"]

        # Get all files and directories, with the exception of anything in .git or .gigantum
        edges = lb.walkdir(section=self._id_data['section'], show_hidden=False)
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
                           "section": self._id_data['section'],
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
        edges = lb.get_favorites(self._id_data['section'])
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
                           "section": self._id_data['section'],
                           "favorite_data": edge}
                edge_objs.append(LabbookFavoriteConnection.Edge(node=LabbookFavorite.create(id_data), cursor=cursor))

            return LabbookFavoriteConnection(edges=edge_objs, page_info=lbc.page_info)
        except Exception as e:
            logger.exception(e)
            raise
