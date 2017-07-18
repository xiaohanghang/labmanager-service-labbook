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
import abc


class ObjectType(graphene.ObjectType):
    """New root object type that enforces standard interface to set and parse Type Ids and populate an instance

    """

    @classmethod
    def get_node(cls, node_id, context, info):
        """Method to get a node from the type ID

        Args:
            node_id(str): The type id for the instance to get
            context:
            info:

        Returns:
            ObjectType
        """
        input_data = {"type_id": node_id}
        return cls.create(input_data)

    @staticmethod
    @abc.abstractmethod
    def to_type_id(id_data):
        """Method to generate a single string that uniquely identifies this object

        Args:
            id_data(dict):

        Returns:
            str
        """
        raise NotImplemented

    @staticmethod
    @abc.abstractmethod
    def parse_type_id(type_id):
        """Method to parse an ID for a given type into its identifiable variables returned as a dictionary of strings

        Args:
            type_id (str): type unique identifier

        Returns:
            dict
        """
        raise NotImplemented

    @staticmethod
    @abc.abstractmethod
    def create(id_data):
        """Method to populate a complete ObjectType instance from a dictionary that uniquely identifies an instances

        Args:
            id_data:

        Returns:

        """
        raise NotImplemented
