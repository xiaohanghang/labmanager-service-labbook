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
import os
import time

import graphene

from lmcommon.configuration import (Configuration, get_docker_client)
from lmcommon.imagebuilder import ImageBuilder
from lmcommon.dispatcher import Dispatcher, jobs
from lmcommon.labbook import LabBook
from lmcommon.labbook.operations import ContainerOps
from lmcommon.logging import LMLogger
from lmcommon.activity.services import stop_labbook_monitor, start_labbook_monitor

from lmsrvcore.auth.user import get_logged_in_username, get_logged_in_author
from lmsrvlabbook.api.objects.environment import Environment


logger = LMLogger.get_logger()


class BuildImage(graphene.relay.ClientIDMutation):
    """Mutator to build a LabBook's Docker Image"""

    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        no_cache = graphene.Boolean(required=False)

    # Return the Environment instance
    environment = graphene.Field(lambda: Environment)

    # The background job key, this may be None
    background_job_key = graphene.Field(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, no_cache=False, client_mutation_id=None):
        username = get_logged_in_username()

        client = get_docker_client()

        labbook_dir = os.path.join(Configuration().config['git']['working_directory'],
                                   username,
                                   owner,
                                   'labbooks',
                                   labbook_name)
        labbook_dir = os.path.expanduser(labbook_dir)
        tag = '{}-{}-{}'.format(username, owner, labbook_name)

        logger.info("BuildImage starting for labbook directory={}, tag={}".format(labbook_dir, tag))

        try:
            image_builder = ImageBuilder(labbook_dir)
            img = image_builder.build_image(docker_client=client, image_tag=tag, username=username, background=True,
                                            nocache=no_cache)
        except Exception as e:
            logger.exception(e)
            raise

        logger.info("Dispatched docker build for labbook directory={}, tag={}, job_key={}"
                    .format(labbook_dir, tag, img.get('background_job_key')))

        return BuildImage(environment=Environment(owner=owner, name=labbook_name),
                          background_job_key=img['background_job_key'])


class StartContainer(graphene.relay.ClientIDMutation):
    """Mutator to start a LabBook's Docker Image in a container"""

    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)

    # Return the Environment instance
    environment = graphene.Field(lambda: Environment)

    # The background job key, this may be None
    background_job_key = graphene.Field(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, client_mutation_id=None):
        username = get_logged_in_username()

        # Load the labbook to retrieve root directory.
        lb = LabBook(author=get_logged_in_author())
        lb.from_name(username, owner, labbook_name)

        container_name = '{}-{}-{}'.format(username, owner, labbook_name)

        lb, keys, ports = ContainerOps.start_container(lb, override_docker_image=container_name, background=True)

        logger.info(f"Dispatched StartContainer to background"
                    f"labbook_dir={lb.key}, job_key={keys.get('background_job_key')}")

        # Start monitoring lab book environment for activity
        start_labbook_monitor(lb, username)

        return StartContainer(environment=Environment(owner=owner, name=labbook_name),
                              background_job_key=keys.get('background_job_key'))


class StopContainer(graphene.relay.ClientIDMutation):
    """Mutation to stop a Docker container. """

    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)

    # Return the Environment instance
    environment = graphene.Field(lambda: Environment)

    # The background job key, this may be None
    background_job_key = graphene.Field(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, client_mutation_id=None):
        username = get_logged_in_username()

        container_name = '{}-{}-{}'.format(username, owner, labbook_name)
        logger.info("Preparing to stop container by name `{}`".format(container_name))

        d = Dispatcher()
        job_ref = d.dispatch_task(jobs.stop_docker_container, args=(container_name,))
        logger.info("Dispatched StopContainer to background, container = `{}`".format(container_name))
        id_data = {"username": username,
                   "owner": owner,
                   "name": labbook_name}

        # Stop monitoring lab book environment for activity
        lb = LabBook(author=get_logged_in_author())
        lb.from_name(username, owner, labbook_name)
        stop_labbook_monitor(lb, username)

        return StopContainer(environment=Environment(owner=owner, name=labbook_name),
                             background_job_key=job_ref)
