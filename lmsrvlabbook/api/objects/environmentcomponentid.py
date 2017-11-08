
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


class EnvironmentComponentClass(graphene.Enum):
    """Enumeration indicating the different classes of Environment Components

    base_image - base docker images
    dev_env - development environments
    package_manager - dependencies installed via package managers
    custom - complex dependencies that are installed via custom docker snippets
    """
    base_image = 0
    dev_env = 1
    package_manager = 2
    custom = 3


class EnvironmentComponent(ObjectType):
    """A type that represents the identifiable information for an environment component"""
    class Meta:
        interfaces = (graphene.relay.Node, )

    # Name of the repository in which this component is stored
    repository = graphene.String()

    # The namespace in the given repository in which this component is stored
    namespace = graphene.String()

    # The the name of the component. Must be unique within the repo/namespace
    name = graphene.String()

    # The COMPONENT spec revision. <major_version>.<minor_version> from the YAML file.
    version = graphene.String()

    # The class of component (e.g. base_image, dev_env)
    component_class = graphene.Field(EnvironmentComponentClass)

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
        if len(split) != 5:
            raise ValueError("Invalid Type ID format. Failed to parse.")

        return {"component_class": split[0], "repo": split[1], "namespace": split[2],
                "component": split[3], "version": split[4]}

    @staticmethod
    def create(id_data):
        """Method to create a graphene Component object based on the type node ID or id data

            id data
            {
                "component_class": class component (e.g. base_image, dev_env),
                "repo": Name of the repository in which this component is stored
                "namespace": The namespace in the given repository in which this component is stored
                "component": The the name of the component. Must be unique within the repo/namespace
                "version": The COMPONENT spec revision. <major_version>.<minor_version> from the YAML file.
            }

        Args:
            id_data(dict): A dictionary of variables that uniquely ID the instance

        Returns:
            EnvironmentAuthor
        """
        if "type_id" in id_data:
            # Parse ID components
            id_data.update(EnvironmentComponent.parse_type_id(id_data["type_id"]))
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

        return EnvironmentComponent(id=EnvironmentComponent.to_type_id(id_data),
                                    repository=component_data["###repository###"],
                                    namespace=component_data["###namespace###"],
                                    name=id_data["component"],
                                    version=id_data["version"],
                                    component_class=EnvironmentComponentClass[id_data['component_class']].value)
