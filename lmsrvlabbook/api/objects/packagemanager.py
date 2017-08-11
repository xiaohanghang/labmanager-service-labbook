
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
from lmsrvcore.api import ObjectType


class PackageManager(ObjectType):
    """A type that represents a Package Manager based Environment Component"""
    class Meta:
        interfaces = (graphene.relay.Node, )

    # The name of the package manager
    package_manager = graphene.String(required=True)

    # The name of the package
    package_name = graphene.String(required=True)

    # The version (optional)
    package_version = graphene.String()

    @staticmethod
    def to_type_id(id_data):
        """Method to generate a single string that uniquely identifies this object

        Args:
            id_data(dict):

        Returns:
            str
        """
        return "{}&{}&{}".format(id_data["component_class"], id_data["package_manager"], id_data["package_name"])

    @staticmethod
    def parse_type_id(type_id):
        """Method to parse an ID for a given type into its identifiable variables returned as a dictionary of strings

        Args:
            type_id (str): type unique identifier

        Returns:
            dict
        """
        split = type_id.split("&")
        if len(split) != 3:
            raise ValueError("Invalid Type ID format. Failed to parse.")

        return {"component_class": split[0], "package_manager": split[1], "package_name": split[2]}

    @staticmethod
    def create(id_data):
        """Method to create a graphene PackageManager object based on the type node ID or id_data

        Args:
            id_data(dict): A dictionary of variables that uniquely ID the instance

        Returns:
            PackageManager
        """
        if "type_id" in id_data:
            # Parse ID components
            id_data.update(PackageManager.parse_type_id(id_data["type_id"]))
            del id_data["type_id"]

        return PackageManager(id=PackageManager.to_type_id(id_data),
                              package_manager=id_data["package_manager"],
                              package_name=id_data["package_name"],
                              package_version=id_data["package_version"])
