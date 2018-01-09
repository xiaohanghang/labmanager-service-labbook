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

from lmsrvcore.api.interfaces import GitRepository
from lmsrvcore.auth.user import get_logged_in_username
from lmsrvcore.api import logged_query
from lmsrvlabbook.dataloader.labbook import LabBookLoader


class LabbookFile(graphene.ObjectType, interfaces=(graphene.relay.Node, GitRepository)):
    """A type representing a file or directory inside the labbook file system."""
    # An instance of the LabBook dataloader
    _dataloader = None
    _file_info = None

    # Section in the LabBook (code, input, output)
    section = graphene.String()

    # Relative path from labbook section.
    key = graphene.String()

    # True indicates that path points to a directory
    is_dir = graphene.Boolean()

    # True indicates that path points to a favorite
    is_favorite = graphene.Boolean()

    # Modified at contains timestamp of last modified - NOT creation - in epoch time.
    modified_at = graphene.Int()

    # Size in bytes.
    size = graphene.Int()

    def _load_file_info(self):
        """Private method to retrieve file info for a given key"""
        if self._file_info:
            # File info is already available in this instance
            file_info = self._file_info
        else:
            # Load file info from LabBook
            if not self.section or not self.key:
                raise ValueError("Must set `section` and `key` on object creation to resolve file info")

            # Load labbook instance
            lb = self._dataloader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").get()

            # Retrieve file info
            file_info = lb.get_file_info(self.section, self.key)

        # Set class properties
        self.is_dir = file_info['is_dir']
        self.modified_at = round(file_info['modified_at'])
        self.size = file_info['size']
        self.is_favorite = file_info['is_favorite']

    @classmethod
    def get_node(cls, info, id):
        """Method to resolve the object based on it's Node ID"""
        # Parse the key
        owner, name, section, key = id.split("&")

        return LabbookFile(id=f"{owner}&{name}&{section}&{key}", name=name, owner=owner, section=section, key=key,
                           _dataloader=LabBookLoader())

    def resolve_id(self, info):
        """Resolve the unique Node id for this object"""
        if not self.id:
            if not self.owner or not self.name or not self.section or not self.key:
                raise ValueError("Resolving a LabbookFile Node ID requires owner, name, section, and key to be set")
            self.id = f"{self.owner}&{self.name}&{self.section}&{self.key}"

        return self.id

    def resolve_is_dir(self, info):
        """Resolve the is_dir field"""
        if self.is_dir is None:
            self._load_file_info()
        return self.is_dir

    def resolve_modified_at(self, info):
        """Resolve the modified_at field"""
        if self.modified_at is None:
            self._load_file_info()
        return self.modified_at

    def resolve_size(self, info):
        """Resolve the size field"""
        if self.size is None:
            self._load_file_info()
        return self.size

    def resolve_is_favorite(self, info):
        """Resolve the is_favorite field"""
        if self.is_favorite is None:
            self._load_file_info()
        return self.is_favorite


class LabbookFavorite(graphene.ObjectType, interfaces=(graphene.relay.Node, GitRepository)):
    """A type representing a file or directory that has been favorited in the labbook file system."""
    # An instance of the LabBook dataloader
    _dataloader = None
    _favorite_data = None

    # Section in the LabBook (code, input, output)
    section = graphene.String()

    # Index value indicating the order of the favorite
    index = graphene.Int()

    # Relative path from labbook root directory.
    key = graphene.String()

    # Short description about the favorite
    description = graphene.String()

    # True indicates that the favorite is a directory
    is_dir = graphene.Boolean()

    def _load_favorite_info(self):
        """Private method to retrieve file info for a given key"""
        if self._favorite_data:
            # File info is already available in this instance
            favorite_data = self._favorite_data
        else:
            # Load file info from LabBook
            if not self.section or not self.index:
                raise ValueError("Must set `section` and `index` on object creation to resolve favorite info")

            # Load labbook instance
            lb = self._dataloader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").get()

            data = lb.get_favorites(self.section)

            # Make sure index is valid
            if self.index > len(data) - 1:
                raise ValueError("Invalid favorite index value")
            if self.index < 0:
                raise ValueError("Invalid favorite index value")

            # Pull out single entry
            favorite_data = data[self.index]

        # Set class properties
        self.description = favorite_data['description']
        self.key = favorite_data['key']
        self.is_dir = favorite_data['is_dir']

    @classmethod
    def get_node(cls, info, id):
        """Method to resolve the object based on it's Node ID"""
        # Parse the key
        owner, name, section, index = id.split("&")

        return LabbookFavorite(id=f"{owner}&{name}&{section}&{index}", name=name, owner=owner, section=section,
                               index=int(index),
                               _dataloader=LabBookLoader())

    def resolve_id(self, info):
        """Resolve the unique Node id for this object"""
        if not self.id:
            if not self.owner or not self.name or not self.section or self.index is None:
                raise ValueError("Resolving a LabbookFavorite Node ID requires owner,name,section, and index to be set")

            self.id = f"{self.owner}&{self.name}&{self.section}&{self.index}"

        return self.id

    def resolve_is_dir(self, info):
        """Resolve the is_dir field"""
        if self.is_dir is None:
            self._load_favorite_info()
        return self.is_dir

    def resolve_key(self, info):
        """Resolve the is_dir field"""
        if self.key is None:
            self._load_favorite_info()
        return self.key

    def resolve_description(self, info):
        """Resolve the is_dir field"""
        if self.description is None:
            self._load_favorite_info()
        return self.description
