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
import os
import time

import graphene
import docker

from lmsrvlabbook.api.objects.environment import Environment
from lmsrvcore.auth.user import get_logged_in_user
from lmcommon.configuration import (Configuration, get_docker_client)
from lmcommon.imagebuilder import ImageBuilder
from lmcommon.labbook import LabBook
from lmcommon.logging import LMLogger

logger = LMLogger.get_logger()


class BuildImage(graphene.relay.ClientIDMutation):
    """Mutator to build a LabBook's Docker Image"""

    class Input:
        owner = graphene.String()
        labbook_name = graphene.String(required=True)

    # Return the Environment instance
    environment = graphene.Field(lambda: Environment)

    # The background job key, this may be None
    background_job_key = graphene.Field(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        # TODO: Lookup name based on logged in user when available
        username = get_logged_in_user()

        if "owner" not in input:
            owner = username
        else:
            owner = input["owner"]

        # TODO: Move environment code into a library
        docker_client_version = os.environ.get("DOCKER_CLIENT_VERSION")

        client = get_docker_client()

        labbook_dir = os.path.join(Configuration().config['git']['working_directory'],
                                   username,
                                   owner,
                                   'labbooks',
                                   input.get('labbook_name'))
        labbook_dir = os.path.expanduser(labbook_dir)
        tag = '{}-{}-{}'.format(username, owner, input.get('labbook_name'))

        logger.info("BuildImage starting for labbook directory={}, tag={}".format(labbook_dir, tag))

        image_builder = ImageBuilder(labbook_dir)
        img = image_builder.build_image(docker_client=client, image_tag=tag, background=True)

        logger.info("Dispatched docker build for labbook directory={}, tag={}, job_key={}"
                    .format(labbook_dir, tag, img.get('background_job_key')))

        id_data = {"username": username,
                   "owner": owner,
                   "name": input.get("labbook_name")}

        env = Environment.create(id_data)
        return BuildImage(environment=env, background_job_key=img['background_job_key'])


class StartContainer(graphene.relay.ClientIDMutation):
    """Mutator to start a LabBook's Docker Image in a container"""

    class Input:
        owner = graphene.String()
        labbook_name = graphene.String(required=True)

    # Return the Environment instance
    environment = graphene.Field(lambda: Environment)

    # The background job key, this may be None
    background_job_key = graphene.Field(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        # TODO: Lookup name based on logged in user when available
        username = get_logged_in_user()

        if "owner" not in input:
            owner = username
        else:
            owner = input["owner"]

        # TODO: Move environment code into a library
        client = get_docker_client()

        # Load the labbook to retrieve root directory.
        lb = LabBook()
        lb.from_name(username, owner, input.get('labbook_name'))
        labbook_dir = lb.root_dir

        container_name = '{}-{}-{}'.format(username, owner, input.get('labbook_name'))
        image_builder = ImageBuilder(labbook_dir)
        cnt = image_builder.run_container(client, container_name, lb, background=True)

        id_data = {"username": username,
                   "owner": owner,
                   "name": input.get("labbook_name")}

        logger.info("Dispatched StartContainer to background, labbook_dir={}, job_key={}".format(
            labbook_dir, cnt.get('background_job_key')))

        return StartContainer(environment=Environment.create(id_data), background_job_key=cnt['background_job_key'])
