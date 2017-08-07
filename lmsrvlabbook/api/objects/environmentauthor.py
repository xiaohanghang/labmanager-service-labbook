
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

from lmcommon.environment import ComponentRepository
from lmsrvcore.api import ObjectType


class EnvironmentAuthor(ObjectType):
    """A type that represents the Author of an environment component"""
    class Meta:
        interfaces = (graphene.relay.Node, )

    # The name of the author
    name = graphene.String(required=True)

    # The email of the author
    email = graphene.String(required=True)

    # The gigantum username of the author
    username = graphene.String(required=True)

    # The organization of the author
    organization = graphene.String()

    @staticmethod
    def to_type_id(id_data):
        """Method to generate a single string that uniquely identifies this object

        Args:
            id_data(dict):

        Returns:
            str
        """
        return "{}&{}&{}&{}&{}".format(id_data["component_class"], id_data["repo"],
                                       id_data["namespace"], id_data["component"], id_data["version"])

    @staticmethod
    def parse_type_id(type_id):
        """Method to parse an ID for a given type into its identifiable variables returned as a dictionary of strings

        Args:
            type_id (str): type unique identifier

        Returns:
            dict
        """
        split = type_id.split("&")
        return {"component_class": split[0], "repo": split[1], "namespace": split[2],
                "component": split[3], "version": split[4]}

    @staticmethod
    def create(id_data):
        """Method to create a graphene EnvironmentAuthor object based on the type node ID or id data

            id data
            {
                "component_class": <unique id for this object Type),
                "repo": <optional username for logged in user>,
                "namespace": <owner username (or org)>,
                "component": <name of the labbook>,
                "version": <name of the labbook>,
                "repo_obj": an instance of an lmcommon.environment.ComponentRepository
            }

        Args:
            id_data(dict): A dictionary of variables that uniquely ID the instance

        Returns:
            EnvironmentAuthor
        """
        if "type_id" in id_data:
            # Parse ID components
            id_data.update(EnvironmentAuthor.parse_type_id(id_data["type_id"]))
            del id_data["type_id"]

        if 'component_data' not in id_data:
            # if component repo does not exist load it
            if 'repo_obj' not in id_data:
                id_data["repo_obj"] = ComponentRepository()

            component_data = id_data["repo_obj"].get_component(id_data["component_class"],
                                                               id_data["repo"],
                                                               id_data["namespace"],
                                                               id_data["component"],
                                                               id_data["version"])
        else:
            # data has already been loaded
            component_data = id_data['component_data']

        return EnvironmentAuthor(id=EnvironmentAuthor.to_type_id(id_data),
                                 name=component_data['author']['name'],
                                 email=component_data['author']['email'],
                                 username=component_data['author']['username'],
                                 organization=component_data['author']['organization'],
                                 )
