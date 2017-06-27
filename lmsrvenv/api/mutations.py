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

import docker
import graphene
from .objects import Environment
from .queries import _get_graphene_environment

from lmcommon.api.util import get_logged_in_user
from lmcommon.configuration import Configuration


class BuildImage(graphene.Mutation):
    """Mutator to build a LabBook's Docker Image"""

    class Input:
        name = graphene.String()

    # Return the Environment instance
    environment = graphene.Field(lambda: Environment)

    @staticmethod
    def mutate(root, args, context, info):
        # TODO: Lookup name based on logged in user when available
        username = get_logged_in_user()

        # TODO: Move environment code into a library
        client = docker.from_env()

        # Get Dockerfile directory
        env_dir = os.path.join(Configuration().config['git']['working_directory'], username,  args.get('name'),
                               '.gigantum', 'env')
        env_dir = os.path.expanduser(env_dir)

        # Build image
        client.images.build(path=env_dir, tag='{}-{}'.format(username, args.get('name')), pull=True)

        return BuildImage(environment=_get_graphene_environment(username, args.get('name')))


class StartContainer(graphene.Mutation):
    """Mutator to start a LabBook's Docker Image in a container"""

    class Input:
        name = graphene.String()

    # Return the Environment instance
    environment = graphene.Field(lambda: Environment)

    @staticmethod
    def mutate(root, args, context, info):
        # TODO: Lookup name based on logged in user when available
        username = get_logged_in_user()

        # TODO: Move environment code into a library
        client = docker.from_env()

        # Get LabBook directory
        labbook_dir = os.path.join(Configuration().config['git']['working_directory'], username,  args.get('name'))
        labbook_dir = os.path.expanduser(labbook_dir)

        # Build image
        client.containers.run('{}-{}'.format(username, args.get('name')),
                              detach=True,
                              name='{}-{}'.format(username, args.get('name')),
                              volumes={labbook_dir: {'bind': '/mnt/labbook', 'mode': 'rw'}})

        return StartContainer(environment=_get_graphene_environment(username, args.get('name')))


class EnvironmentMutations(graphene.AbstractType):
    """Entry point for all Environment graphql mutations"""
    build_image = BuildImage.Field()
    start_container = StartContainer.Field()
