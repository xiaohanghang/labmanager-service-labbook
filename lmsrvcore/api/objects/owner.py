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
from lmsrvcore.api.interfaces import User
from lmsrvcore.api import ObjectType


class Owner(ObjectType, interfaces=(graphene.relay.Node, User)):
    """A type representing the owner (namespace) of a LabBook or Dataset"""

    @staticmethod
    def to_type_id(namespace: str) -> str:
        """Method to generate a single string that uniquely identifies this object

        Args:
            namespace(str): Gigantum username or organization name of the owner (a.k.a. namespace)

        Returns:
            str
        """
        return namespace

    @staticmethod
    def parse_type_id(type_id: str) -> dict:
        """Method to parse an ID for a given type into its identifiable variables returned as a dictionary of strings

        Args:
            namespace(str): type unique identifier

        Returns:
            dict
        """
        return {'namespace': type_id}

    @staticmethod
    def create(namespace: str) -> 'Owner':
        """Method to populate a complete Owner instance

        Args:
            namespace(str): Gigantum username or organization name of the owner (a.k.a. namespace)

        Returns:
            Owner
        """
        return Owner(id=Owner.to_type_id(namespace),
                     username=namespace)


class OwnerInput(graphene.InputObjectType):
    """The input type to create a new Owner or LabBook fields that use Owner"""
    namespace = graphene.String()
