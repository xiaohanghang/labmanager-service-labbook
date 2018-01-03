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
    # A dataloader instance for the object type
    _loader = None

    @classmethod
    def get_node(cls, info, type_id):
        """Method to get a node from the type ID

        Args:
            type_id(str): The type id for the instance to get
            info: Graphene info object

        Returns:
            ObjectType
        """
        # Convert from type id to kwargs required to create
        kwargs = cls.parse_type_id(type_id)

        # Call create
        return cls.create(**kwargs)

    @staticmethod
    @abc.abstractmethod
    def to_type_id(**kwargs):
        """Method to generate a single string that uniquely identifies this object using the delimiter

        Args:

        Returns:
            str
        """
        raise NotImplemented

    @staticmethod
    @abc.abstractmethod
    def parse_type_id(type_id: str):
        """Method to parse a type ID for a given type into its identifiable variables returned as a dictionary of strings

        Args:
            type_id (str): type unique identifier

        Returns:
            dict
        """
        raise NotImplemented

    @staticmethod
    @abc.abstractmethod
    def create(**kwargs):
        """Method to instantiate and prep an ObjectType instance from kwargs that uniquely identifies the instance

        Args:
            kwargs: Keyword args required to identify and create the object

        Returns:
            ObjectType
        """
        raise NotImplemented
