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

import graphene
import docker

from lmsrvlabbook.api.objects.environment import Environment
from lmsrvcore.auth.user import get_logged_in_user
from lmcommon.configuration import Configuration
from lmcommon.imagebuilder import ImageBuilder


class BuildImage(graphene.relay.ClientIDMutation):
    """Mutator to build a LabBook's Docker Image"""

    class Input:
        owner = graphene.String()
        labbook_name = graphene.String(required=True)

    # Return the Environment instance
    environment = graphene.Field(lambda: Environment)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        # TODO: Lookup name based on logged in user when available
        username = get_logged_in_user()

        if "owner" not in input:
            owner = username
        else:
            owner = input["username"]

        # TODO: Move environment code into a library
        docker_client_version = os.environ.get("DOCKER_CLIENT_VERSION")

        if docker_client_version:
            # This is needed for CircleCI, may be needed for other deployment envs as well.
            client = docker.from_env(version=docker_client_version)
        else:
            client = docker.from_env()

        labbook_dir = os.path.join(Configuration().config['git']['working_directory'], username, owner,
                               input.get('labbook_name'))
        labbook_dir = os.path.expanduser(labbook_dir)

        tag='{}-{}-{}'.format(username, owner, input.get('labbook_name'))
        image_builder = ImageBuilder(labbook_dir)
        docker_image = image_builder.build_image(docker_client=client, tag=tag)

        id_data = {"username": username,
                   "owner": owner,
                   "name": input.get("labbook_name")}
        
        return BuildImage(environment=Environment.create(id_data))


class StartContainer(graphene.relay.ClientIDMutation):
    """Mutator to start a LabBook's Docker Image in a container"""

    class Input:
        owner = graphene.String()
        labbook_name = graphene.String(required=True)

    # Return the Environment instance
    environment = graphene.Field(lambda: Environment)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        # TODO: Lookup name based on logged in user when available
        username = get_logged_in_user()

        if "owner" not in input:
            owner = username
        else:
            owner = input["username"]

        # TODO: Move environment code into a library
        client = docker.from_env()

        # Get Dockerfile directory
        labbook_dir = os.path.join(Configuration().config['git']['working_directory'],
                                   username, owner,
                                   input.get('labbook_name'))
        labbook_dir = os.path.expanduser(labbook_dir)

        # Start container
        client.containers.run('{}-{}-{}'.format(username, owner, input.get('labbook_name')),
                              detach=True,
                              name='{}-{}-{}'.format(username, owner, input.get('labbook_name')),
                              ports={"8888/tcp": "8888"},
                              volumes={labbook_dir: {'bind': '/mnt/labbook', 'mode': 'rw'}})

        id_data = {"username": username,
                   "owner": owner,
                   "name": input.get("labbook_name")}

        return BuildImage(environment=Environment.create(id_data))

