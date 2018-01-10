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
from lmsrvcore.api import logged_query
from lmsrvcore.api.interfaces import GitRepository
from lmsrvcore.api.connections import ListBasedConnection

from lmsrvlabbook.api.objects.labbookfile import LabbookFavorite, LabbookFile
from lmsrvlabbook.api.connections.labbookfileconnection import LabbookFileConnection, LabbookFavoriteConnection
from lmsrvlabbook.dataloader.labbook import LabBookLoader

logger = LMLogger.get_logger()


class LabbookSection(graphene.ObjectType, interfaces=(graphene.relay.Node, GitRepository)):
    """A type representing a section within a LabBook (i.e., code, input, output)
    """
    # A copy of the LabBook dataloader
    _dataloader = None

    # Section name (code, input, output)
    section = graphene.String()

    # List of files and directories, given a relative root directory within the section
    files = graphene.relay.ConnectionField(LabbookFileConnection, root_dir=graphene.String())

    # List of all files and directories within the section
    all_files = graphene.relay.ConnectionField(LabbookFileConnection)

    # List of favorites for a given subdir (code, input, output)
    favorites = graphene.relay.ConnectionField(LabbookFavoriteConnection)

    @classmethod
    def get_node(cls, info, id):
        """Method to resolve the object based on it's Node ID"""
        # Parse the key
        owner, name, section = id.split("&")

        return LabbookSection(owner=owner, name=name, section=section, _dataloader=LabBookLoader())

    def resolve_id(self, info):
        """Resolve the unique Node id for this object"""
        if not self.id:
            if not self.owner or not self.name or not self.section:
                raise ValueError("Resolving a LabbookFavorite Node ID requires owner, name, and section to be set")

            self.id = f"{self.owner}&{self.name}&{self.section}"

        return self.id

    def resolve_files(self, info, **kwargs):
        """Resolver for getting file listing in a single directory"""
        lb = self._dataloader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").get()

        base_dir = None
        if 'root_dir' in kwargs:
            if kwargs['root_dir']:
                base_dir = kwargs['root_dir'] + os.path.sep
                base_dir = base_dir.replace(os.path.sep + os.path.sep, os.path.sep)

        # Get all files and directories, with the exception of anything in .git or .gigantum
        edges = lb.listdir(self.section, base_path=base_dir, show_hidden=False)

        # Generate naive cursors
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, kwargs)
        lbc.apply()

        edge_objs = []
        for edge, cursor in zip(lbc.edges, lbc.cursors):
            create_data = {"owner": self.owner,
                           "section": self.section,
                           "name": self.name,
                           "key": edge['key'],
                           "_dataloader": self._dataloader,
                           "_file_info": edge}
            edge_objs.append(LabbookFileConnection.Edge(node=LabbookFile(**create_data), cursor=cursor))

        return LabbookFileConnection(edges=edge_objs, page_info=lbc.page_info)

    def resolve_all_files(self, info, **kwargs):
        """Resolver for getting all files in a LabBook section"""
        lb = self._dataloader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").get()

        # Get all files and directories, with the exception of anything in .git or .gigantum
        edges = lb.walkdir(section=self.section, show_hidden=False)
        # Generate naive cursors
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, kwargs)
        lbc.apply()

        edge_objs = []
        for edge, cursor in zip(lbc.edges, lbc.cursors):
            create_data = {"owner": self.owner,
                           "section": self.section,
                           "name": self.name,
                           "key": edge['key'],
                           "_dataloader": self._dataloader,
                           "_file_info": edge}
            edge_objs.append(LabbookFileConnection.Edge(node=LabbookFile(**create_data), cursor=cursor))

        return LabbookFileConnection(edges=edge_objs, page_info=lbc.page_info)

    def resolve_favorites(self, info, **kwargs):
        """Resolve all favorites for the given section"""
        lb = self._dataloader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").get()

        # Get all files and directories, with the exception of anything in .git or .gigantum
        edges = lb.get_favorites(self.section)
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, kwargs)
        lbc.apply()

        edge_objs = []
        for edge, cursor in zip(lbc.edges, lbc.cursors):
            create_data = {"id": f"{self.owner}&{self.name}&{self.section}&{edge['index']}",
                           "owner": self.owner,
                           "section": self.section,
                           "name": self.name,
                           "index": int(edge['index']),
                           "_dataloader": self._dataloader,
                           "_favorite_data": edge}
            edge_objs.append(LabbookFavoriteConnection.Edge(node=LabbookFavorite(**create_data), cursor=cursor))

        return LabbookFavoriteConnection(edges=edge_objs, page_info=lbc.page_info)
