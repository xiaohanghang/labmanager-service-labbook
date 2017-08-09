
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

from lmsrvlabbook.api.objects.environmentauthor import EnvironmentAuthor
from lmsrvlabbook.api.objects.environmentinfo import EnvironmentInfo
from lmsrvlabbook.api.objects.environmentcomponentid import EnvironmentComponent

from lmcommon.environment import ComponentRepository

from lmsrvcore.api import ObjectType


class DevEnv(ObjectType):
    """A type that represents a Development Environment Environment Component"""
    class Meta:
        interfaces = (graphene.relay.Node, )

    # Component ID information for supporting Mutations
    component = graphene.Field(EnvironmentComponent, required=True)

    # The name of the current branch
    author = graphene.Field(EnvironmentAuthor, required=True)

    # The name of the current branch
    info = graphene.Field(EnvironmentInfo, required=True)

    # The class of Operating System this works with (e.g. ubuntu)
    os_base_class = graphene.String(required=True)

    # The type of development environment (e.g. web, xforward)
    development_environment_class = graphene.String(required=True)

    # The installation commands for the docker file
    install_commands = graphene.List(graphene.String, required=True)

    # The image tag to use on the container registry server when pulling the image
    exec_commands = graphene.List(graphene.String, required=True)

    # The image tag to use on the container registry server when pulling the image
    exposed_tcp_ports = graphene.List(graphene.String, required=True)

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
        """Method to create a graphene DevEnv object based on the type node ID or id_data

        Args:
            id_data(dict): A dictionary of variables that uniquely ID the instance

        Returns:
            Environment
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

        return DevEnv(id=DevEnv.to_type_id(id_data),
                      author=EnvironmentAuthor.create(id_data),
                      info=EnvironmentInfo.create(id_data),
                      component=EnvironmentComponent.create(id_data),
                      os_base_class=component_data['os_base_class'],
                      development_environment_class=component_data['development_environment_class'],
                      install_commands=component_data['install_commands'],
                      exec_commands=component_data['exec_commands'],
                      exposed_tcp_ports=component_data['exposed_tcp_ports'])
