
# Copyright (c) 2018 FlashX, LLC
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
import base64

import docker
from docker.errors import ImageNotFound, NotFound
import requests

from lmcommon.dispatcher import Dispatcher
from lmcommon.environment.componentmanager import ComponentManager
from lmcommon.configuration import get_docker_client
from lmcommon.logging import LMLogger

from lmsrvcore.api.interfaces import GitRepository
from lmsrvcore.auth.user import get_logged_in_username
from lmsrvcore.api.connections import ListBasedConnection

from lmsrvlabbook.api.connections.environment import CustomComponentConnection, PackageComponentConnection
from lmsrvlabbook.api.objects.basecomponent import BaseComponent
from lmsrvlabbook.api.objects.packagecomponent import PackageComponent
from lmsrvlabbook.api.objects.customcomponent import CustomComponent

logger = LMLogger.get_logger()


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

    # The image failed to build
    BUILD_FAILED = 4


class ContainerStatus(graphene.Enum):
    """An enumeration for container image status"""

    # The container is not running
    NOT_RUNNING = 0

    # The container is starting
    STARTING = 1

    # The container is running
    RUNNING = 2


class Environment(graphene.ObjectType, interfaces=(graphene.relay.Node, GitRepository)):
    """A type that represents the Environment for a LabBook"""
    # The name of the current branch
    image_status = graphene.Field(ImageStatus)

    # The name of the current branch
    container_status = graphene.Field(ContainerStatus)

    # The LabBook's Base Component
    base = graphene.Field(BaseComponent)

    # The LabBook's Package manager installed dependencies
    package_dependencies = graphene.ConnectionField(PackageComponentConnection)

    # The LabBook's Custom dependencies
    custom_dependencies = graphene.ConnectionField(CustomComponentConnection)

    @classmethod
    def get_node(cls, info, id):
        """Method to resolve the object based on it's Node ID"""
        # Parse the key
        owner, name = id.split("&")

        return Environment(id=f"{owner}&{name}", name=name, owner=owner)

    def resolve_id(self, info):
        """Resolve the unique Node id for this object"""
        if not self.owner or not self.name:
            raise ValueError("Resolving a Environment Node ID requires owner and name to be set")

        return f"{self.owner}&{self.name}"

    def resolve_image_status(self, info):
        """Resolve the image_status field"""
        labbook_key = "{}-{}-{}".format(get_logged_in_username(), self.owner, self.name)

        dispatcher = Dispatcher()
        lb_jobs = [dispatcher.query_task(j.job_key) for j in dispatcher.get_jobs_for_labbook(labbook_key)]

        for j in lb_jobs:
            logger.debug("Current job for lb: status {}, meta {}".format(j.status, j.meta))

        # First, check if image exists or not -- The first step of building an image untags any existing ones.
        # Therefore, we know that if one exists, there most likely is not one being built.
        try:
            client = get_docker_client()
            client.images.get(labbook_key)
            image_status = ImageStatus.EXISTS
        except (ImageNotFound, requests.exceptions.ConnectionError):
            image_status = ImageStatus.DOES_NOT_EXIST

        if any([j.status == 'failed' and j.meta.get('method') == 'build_image' for j in lb_jobs]):
            logger.info("Image status for {} is BUILD_FAILED".format(labbook_key))
            if image_status == ImageStatus.EXISTS:
                # The indication that there's a failed job is probably lingering from a while back, so don't
                # change the status to FAILED. Only do that if there is no Docker image.
                logger.warning(f'Got failed build_image for labbook {labbook_key}, but image exists.')
            else:
                image_status = ImageStatus.BUILD_FAILED

        if any([j.status in ['started', 'queued'] and j.meta.get('method') == 'build_image' for j in lb_jobs]):
            logger.info(f"Image status for {labbook_key} is BUILD_IN_PROGRESS")
            # build_image being in progress takes precedence over if image already exists (unlikely event).
            if image_status == ImageStatus.EXISTS:
                logger.warning(f'Got started/queued build_image for labbook {labbook_key}, but image exists.')
            image_status = ImageStatus.BUILD_IN_PROGRESS

        return image_status.value

    def resolve_container_status(self, info):
        """Resolve the image_status field"""
        # Check if the container is running by looking up the container
        labbook_key = "{}-{}-{}".format(get_logged_in_username(), self.owner, self.name)

        try:
            client = get_docker_client()
            container = client.containers.get(labbook_key)
            if container.status == "running":
                container_status = ContainerStatus.RUNNING
            else:
                container_status = ContainerStatus.NOT_RUNNING
        except (NotFound, requests.exceptions.ConnectionError):
            container_status = ContainerStatus.NOT_RUNNING

        return container_status.value

    def resolve_base_image(self, info):
        """Method to get the LabBook's base component

        Args:
            info:

        Returns:

        """
        # Get base image data
        lb = info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").get()
        cm = ComponentManager(lb)

        component_data = cm.get_component_list("base_image")

        if component_data:
            component_data = component_data[0]
            return BaseComponent(id=f"{component_data['###repository###']}&{component_data['id']}&{component_data['revision']}",
                                 repository=component_data['###repository###'],
                                 component_id=component_data['id'],
                                 revision=int(component_data['revision']))
        else:
            return None

    def resolve_package_dependencies(self, info, **kwargs):
        """Method to get the LabBook's package manager dependencies

        Args:
            info:

        Returns:

        """
        lb = info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").get()
        cm = ComponentManager(lb)

        edges = cm.get_component_list("package_manager")

        if edges:
            cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in
                       enumerate(edges)]

            # Process slicing and cursor args
            lbc = ListBasedConnection(edges, cursors, kwargs)
            lbc.apply()

            # Get DevEnv instances
            edge_objs = []
            for edge, cursor in zip(lbc.edges, lbc.cursors):
                edge_objs.append(PackageComponentConnection.Edge(node=PackageComponent(owner=self.owner,
                                                                                       name=self.name,
                                                                                       manager=edge['package_manager'],
                                                                                       package=edge['name'],
                                                                                       revision=edge['revision']),
                                                   cursor=cursor))

            return PackageComponentConnection(edges=edge_objs, page_info=lbc.page_info)

        else:
            return PackageComponentConnection(edges=[], page_info=graphene.relay.PageInfo(has_next_page=False,
                                                                                          has_previous_page=False))

    def resolve_custom_dependencies(self, info, **kwargs):
        """Method to get the LabBook's custom dependencies

        Args:
            info:

        Returns:

        """
        lb = info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").get()
        cm = ComponentManager(lb)

        edges = cm.get_component_list("custom")

        if edges:
            cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in
                       enumerate(edges)]

            # Process slicing and cursor args
            lbc = ListBasedConnection(edges, cursors, kwargs)
            lbc.apply()

            # Get DevEnv instances
            edge_objs = []
            for edge, cursor in zip(lbc.edges, lbc.cursors):
                edge_objs.append(CustomComponentConnection.Edge(node=CustomComponent(owner=self.owner,
                                                                                     name=self.name,
                                                                                     repository=edge['###repository###'],
                                                                                     component_id=edge['id'],
                                                                                     revision=edge['revision']),
                                                                cursor=cursor))

            return CustomComponentConnection(edges=edge_objs, page_info=lbc.page_info)

        else:
            return CustomComponentConnection(edges=[], page_info=graphene.relay.PageInfo(has_next_page=False,
                                                                                         has_previous_page=False))

