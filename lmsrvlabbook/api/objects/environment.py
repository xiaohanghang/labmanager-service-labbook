
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

import docker
from docker.errors import ImageNotFound, NotFound

from lmsrvcore.auth.user import get_logged_in_user

from lmsrvcore.api import ObjectType


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
        client = docker.from_env()

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
