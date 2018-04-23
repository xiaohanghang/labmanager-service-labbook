# Copyright (c) 2018 FlashX, LLC
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


class RemoteLabbook(graphene.ObjectType, interfaces=(graphene.relay.Node, GitRepository)):
    """A type representing a LabBook stored on a remote server

    RemoteLabbooks are uniquely identified by both the "owner" and the "name" of the LabBook

    NOTE: RemoteLabbooks require all fields to be explicitly set as there is no current way to asynchronously retrieve
          the data

    NOTE: Currently all description fields will return empty strings

    """
    # A short description of the LabBook limited to 140 UTF-8 characters
    description = graphene.String()

    # Creation date/timestamp in UTC in ISO format
    creation_date_utc = graphene.String()

    # Modification date/timestamp in UTC in ISO format
    modified_date_utc = graphene.String()

    @classmethod
    def get_node(cls, info, id):
        """Method to resolve the object based on it's Node ID"""
        # Parse the key
        owner, name = id.split("&")

        return RemoteLabbook(id="{}&{}".format(owner, name), name=name, owner=owner)

    def resolve_id(self, info):
        """Resolve the unique Node id for this object"""
        if not self.id:
            if not self.owner or not self.name:
                raise ValueError("Resolving a Remote Labbook Node ID requires owner and name to be set")
            self.id = f"{self.owner}&{self.name}"
        return self.id

    def resolve_description(self, info):
        """Return the description of the labbook"""
        if self.description is None:
            raise ValueError("RemoteLabbook requires all fields to be explicitly set")
        return self.description

    def resolve_creation_date_utc(self, info):
        """Return the creation timestamp

        Args:
            info:

        Returns:

        """
        if self.creation_date_utc is None:
            raise ValueError("RemoteLabbook requires all fields to be explicitly set")
        return self.creation_date_utc

    def resolve_modified_date_utc(self, info):
        """Return the modified timestamp

        Args:
            info:

        Returns:

        """
        if self.modified_date_utc is None:
            raise ValueError("RemoteLabbook requires all fields to be explicitly set")
        return self.modified_date_utc
