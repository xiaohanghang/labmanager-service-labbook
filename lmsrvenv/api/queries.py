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
import docker
import graphene
from docker.errors import ImageNotFound, NotFound
from graphene import resolve_only_args

from lmsrvcore.api import get_logged_in_user
from .objects import Environment, ContainerStatus, ImageStatus


def _get_graphene_environment(username, labbook_name):
    """Method to get an Environment instance

    Args:
        username(str): The username to use when looking up containers and images
        labbook_name(str): The name of the LabBook you are interacting with

    Returns:
        Environment
    """
    # TODO: Move environment interaction to a library
    client = docker.from_env()

    # Check if the image exists
    try:
        client.images.get("{}-{}".format(username, labbook_name))
        image_status = ImageStatus.EXISTS
    except ImageNotFound:
        image_status = ImageStatus.DOES_NOT_EXIST

    # Check if the container is running by looking up the container
    try:
        container = client.containers.get("{}-{}".format(username, labbook_name))
        if container.status == "running":
            container_status = ContainerStatus.RUNNING
        else:
            container_status = ContainerStatus.NOT_RUNNING
    except NotFound:
        container_status = ContainerStatus.NOT_RUNNING

    return Environment(image_status=image_status.value, container_status=container_status.value)


class EnvironmentQueries(graphene.AbstractType):
    """Entry point for all LabBook Environment queries"""
    environment = graphene.Field(Environment, name=graphene.String())

    @resolve_only_args
    def resolve_environment(self, name):
        """Method to return a graphene Environment instance based on the name of the LabBook

        Uses the "currently logged in" user

        Args:
            name(str): Name of the LabBook

        Returns:
            Environment
        """
        # TODO: Lookup name based on logged in user when available
        username = get_logged_in_user()

        return _get_graphene_environment(username, name)


