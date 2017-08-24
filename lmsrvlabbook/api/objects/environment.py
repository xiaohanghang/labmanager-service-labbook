
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
import os
import base64

import docker
from docker.errors import ImageNotFound, NotFound

from lmcommon.environment.componentmanager import ComponentManager
from lmcommon.labbook import LabBook
from lmcommon.configuration import get_docker_client

from lmsrvcore.auth.user import get_logged_in_user
from lmsrvcore.api import ObjectType
from lmsrvcore.api.connections import ListBasedConnection

from lmsrvlabbook.api.objects.environmentauthor import EnvironmentAuthor
from lmsrvlabbook.api.objects.environmentinfo import EnvironmentInfo
from lmsrvlabbook.api.objects.environmentcomponentid import EnvironmentComponent
from lmsrvlabbook.api.connections.devenv import DevEnvConnection, DevEnv
from lmsrvlabbook.api.connections.customdependency import CustomDependencyConnection, CustomDependency
from lmsrvlabbook.api.connections.packagemanager import PackageManagerConnection, PackageManager
from lmsrvlabbook.api.objects.baseimage import BaseImage


class ImageStatus(graphene.Enum):
    """An enumeration for Docker image status"""
    # The image has not be built locally yet
    DOES_NOT_EXIST = 0
    # The image is being built
    BUILD_IN_PROGRESS = 1
    # The image has been built and the Dockerfile has yet to change
    EXISTS = 2
    # The image has been built and the Dockerfile has been edited
    STALE = 3


class ContainerStatus(graphene.Enum):
    """An enumeration for container image status"""
    # The container is not running
    NOT_RUNNING = 0
    # The container is starting
    STARTING = 1
    # The container is running
    RUNNING = 2


class Environment(ObjectType):
    """A type that represents the Environment for a LabBook"""
    class Meta:
        interfaces = (graphene.relay.Node, )

    # The name of the current branch
    image_status = graphene.Field(ImageStatus)

    # The name of the current branch
    container_status = graphene.Field(ContainerStatus)

    # The LabBook's Base Image
    base_image = graphene.Field(BaseImage)

    # The LabBook's Dev Envs
    dev_envs = graphene.ConnectionField(DevEnvConnection)

    # The LabBook's Package manager installed dependencies
    package_manager_dependencies = graphene.ConnectionField(PackageManagerConnection)

    # The LabBook's Custom dependencies
    custom_dependencies = graphene.ConnectionField(CustomDependencyConnection)

    @staticmethod
    def to_type_id(id_data):
        """Method to generate a single string that uniquely identifies this object

        Args:
            id_data(dict):

        Returns:
            str
        """
        return "{}&{}&{}".format(id_data["username"], id_data["owner"], id_data["name"])

    @staticmethod
    def parse_type_id(type_id):
        """Method to parse an ID for a given type into its identifiable variables returned as a dictionary of strings

        Args:
            type_id (str): type unique identifier

        Returns:
            dict
        """
        split = type_id.split("&")
        return {"username": split[0], "owner": split[1], "name": split[2]}

    @staticmethod
    def create(id_data):
        """Method to create a graphene LabBookCommit object based on the type node ID or owner+name+hash

        id_data should at a minimum contain either `type_id` or `owner` & `name` & `hash`

            {
                "type_id": <unique id for this object Type),
                "username": <optional username for logged in user>,
                "owner": <owner username (or org)>,
                "name": <name of the labbook>,
            }

        Args:
            id_data(dict): A dictionary of variables that uniquely ID the instance

        Returns:
            Environment
        """
        if "username" not in id_data:
            # TODO: Lookup name based on logged in user when available
            id_data["username"] = get_logged_in_user()

        if "type_id" in id_data:
            # Parse ID components
            id_data.update(Environment.parse_type_id(id_data["type_id"]))
            del id_data["type_id"]

        # TODO: Move environment interaction to a library
        docker_client_version = os.environ.get("DOCKER_CLIENT_VERSION")

        client = get_docker_client()

        # Check if the image exists
        try:
            client.images.get("{}-{}-{}".format(id_data["username"], id_data["owner"], id_data["name"]))
            image_status = ImageStatus.EXISTS
        except ImageNotFound:
            image_status = ImageStatus.DOES_NOT_EXIST

        # Check if the container is running by looking up the container
        try:
            container = client.containers.get("{}-{}-{}".format(id_data["username"], id_data["owner"], id_data["name"]))
            if container.status == "running":
                container_status = ContainerStatus.RUNNING
            else:
                container_status = ContainerStatus.NOT_RUNNING
        except NotFound:
            container_status = ContainerStatus.NOT_RUNNING

        return Environment(id=Environment.to_type_id(id_data),
                           image_status=image_status.value, container_status=container_status.value)

    def resolve_base_image(self, args, context, info):
        """Method to get the LabBook's base image

        Args:
            args:
            context:
            info:

        Returns:

        """
        # TODO: Implement better method to share data between resolvers
        # The id field is populated at this point, so should be able to use that info for now
        id_data = {"username": get_logged_in_user()}
        id_data.update(Environment.parse_type_id(self.id))

        # Get base image data
        lb = LabBook()
        lb.from_name(id_data["username"], id_data["owner"], id_data["name"])
        cm = ComponentManager(lb)

        component_data = cm.get_component_list("base_image")

        if component_data:
            component_data = component_data[0]
            # Switch ID data to a BaseImage
            id_data["component_class"] = "base_image"
            id_data["repo"] = component_data["###repository###"]
            id_data["namespace"] = component_data["###namespace###"]
            id_data["component"] = component_data['info']['name']
            id_data["version"] = "{}.{}".format(component_data['info']['version_major'],
                                                component_data['info']['version_minor'])

            package_managers = [pm['name'] for pm in component_data['available_package_managers']]

            return BaseImage(id=BaseImage.to_type_id(id_data),
                             author=EnvironmentAuthor.create(id_data),
                             info=EnvironmentInfo.create(id_data),
                             component=EnvironmentComponent.create(id_data),
                             os_class=component_data['os_class'],
                             os_release=component_data['os_release'],
                             server=component_data['image']['server'],
                             namespace=component_data['image']['namespace'],
                             repository=component_data['image']['repo'],
                             tag=component_data['image']['tag'],
                             available_package_managers=package_managers)
        else:
            return None

    def resolve_dev_envs(self, args, context, info):
        """Method to get the LabBook's dev envs

        Args:
            args:
            context:
            info:

        Returns:

        """
        # TODO: Implement better method to share data between resolvers
        # The id field is populated at this point, so should be able to use that info for now
        id_data = {"username": get_logged_in_user()}
        id_data.update(Environment.parse_type_id(self.id))

        # Get base image data
        lb = LabBook()
        lb.from_name(id_data["username"], id_data["owner"], id_data["name"])
        cm = ComponentManager(lb)

        edges = cm.get_component_list("dev_env")

        if edges:
            cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in
                       enumerate(edges)]

            # Process slicing and cursor args
            lbc = ListBasedConnection(edges, cursors, args)
            lbc.apply()

            # Get DevEnv instances
            edge_objs = []
            for edge, cursor in zip(lbc.edges, lbc.cursors):
                id_data = {'component_data': edge,
                           'component_class': 'dev_env',
                           'repo': edge['###repository###'],
                           'namespace': edge['###namespace###'],
                           'component': edge['info']['name'],
                           'version': "{}.{}".format(edge['info']['version_major'], edge['info']['version_minor'])
                           }
                edge_objs.append(DevEnvConnection.Edge(node=DevEnv.create(id_data), cursor=cursor))

            return DevEnvConnection(edges=edge_objs, page_info=lbc.page_info)

        else:
            return DevEnvConnection(edges=[], page_info=graphene.relay.PageInfo(has_next_page=False,
                                                                                has_previous_page=False))

    def resolve_package_manager_dependencies(self, args, context, info):
        """Method to get the LabBook's package manager deps

        Args:
            args:
            context:
            info:

        Returns:

        """
        # TODO: Implement better method to share data between resolvers
        # The id field is populated at this point, so should be able to use that info for now
        id_data = {"username": get_logged_in_user()}
        id_data.update(Environment.parse_type_id(self.id))

        # Get base image data
        lb = LabBook()
        lb.from_name(id_data["username"], id_data["owner"], id_data["name"])
        cm = ComponentManager(lb)

        edges = cm.get_component_list("package_manager")

        if edges:
            cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in
                       enumerate(edges)]

            # Process slicing and cursor args
            lbc = ListBasedConnection(edges, cursors, args)
            lbc.apply()

            # Get DevEnv instances
            edge_objs = []
            for edge, cursor in zip(lbc.edges, lbc.cursors):
                id_data = {'component_data': edge,
                           'component_class': 'package_manager',
                           'package_manager': edge['package_manager'],
                           'package_name': edge['name'],
                           'package_version': edge['version']
                           }
                edge_objs.append(PackageManagerConnection.Edge(node=PackageManager.create(id_data), cursor=cursor))

            return PackageManagerConnection(edges=edge_objs, page_info=lbc.page_info)

        else:
            return PackageManagerConnection(edges=[], page_info=graphene.relay.PageInfo(has_next_page=False,
                                                                                        has_previous_page=False))

    def resolve_custom_dependencies(self, args, context, info):
        """Method to get the LabBook's custom deps

        Args:
            args:
            context:
            info:

        Returns:

        """
        # TODO: Implement better method to share data between resolvers
        # The id field is populated at this point, so should be able to use that info for now
        id_data = {"username": get_logged_in_user()}
        id_data.update(Environment.parse_type_id(self.id))

        # Get base image data
        lb = LabBook()
        lb.from_name(id_data["username"], id_data["owner"], id_data["name"])
        cm = ComponentManager(lb)

        edges = cm.get_component_list("custom")

        if edges:
            cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in
                       enumerate(edges)]

            # Process slicing and cursor args
            lbc = ListBasedConnection(edges, cursors, args)
            lbc.apply()

            # Get DevEnv instances
            edge_objs = []
            for edge, cursor in zip(lbc.edges, lbc.cursors):
                id_data = {'component_data': edge,
                           'component_class': 'custom',
                           'repo': edge['###repository###'],
                           'namespace': edge['###namespace###'],
                           'component': edge['info']['name'],
                           'version': "{}.{}".format(edge['info']['version_major'], edge['info']['version_minor'])
                           }
                edge_objs.append(CustomDependencyConnection.Edge(node=CustomDependency.create(id_data), cursor=cursor))

            return CustomDependencyConnection(edges=edge_objs, page_info=lbc.page_info)

        else:
            return CustomDependencyConnection(edges=[], page_info=graphene.relay.PageInfo(has_next_page=False,
                                                                                          has_previous_page=False))
