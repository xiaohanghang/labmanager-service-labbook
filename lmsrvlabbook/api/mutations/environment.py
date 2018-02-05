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
import graphene

from lmcommon.configuration import Configuration
from lmcommon.imagebuilder import ImageBuilder
from lmcommon.dispatcher import Dispatcher, jobs
from lmcommon.labbook import LabBook
from lmcommon.container import ContainerOperations
from lmcommon.logging import LMLogger
from lmcommon.activity.services import stop_labbook_monitor

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
        labbook_dir = os.path.expanduser(os.path.join(Configuration().config['git']['working_directory'],
                                         username, owner, 'labbooks', labbook_name))

        lb = LabBook(author=get_logged_in_author())
        lb.from_directory(labbook_dir)

        # Generate Dockerfile
        ib = ImageBuilder(labbook_directory=labbook_dir)
        ib.assemble_dockerfile(write=True)

        # Kick off building in a background thread
        d = Dispatcher()
        build_kwargs = {
            'path': labbook_dir,
            'username': username,
            'nocache': no_cache
        }

        metadata = {'labbook': lb.key,
                    'method': 'build_image'}

        res = d.dispatch_task(jobs.build_labbook_image, kwargs=build_kwargs, metadata=metadata)

        return BuildImage(environment=Environment(owner=owner, name=labbook_name),
                          background_job_key=res.key_str)


class StartContainer(graphene.relay.ClientIDMutation):
    """Mutator to start a LabBook's Docker Image in a container"""

    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)

    # Return the Environment instance
    environment = graphene.Field(lambda: Environment)

    @classmethod
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, client_mutation_id=None):
        username = get_logged_in_username()
        lb = LabBook(author=get_logged_in_author())
        lb.from_name(username, owner, labbook_name)

        lb, container_id, ports = ContainerOperations.start_container(labbook=lb, username=username)
        logger.info(f'Started new {lb} container ({container_id}) with ports {ports}')

        return StartContainer(environment=Environment(owner=owner, name=labbook_name))


class StopContainer(graphene.relay.ClientIDMutation):
    """Mutation to stop a Docker container. """

    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)

    # Return the Environment instance
    environment = graphene.Field(lambda: Environment)

    @classmethod
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, client_mutation_id=None):
        username = get_logged_in_username()
        lb = LabBook(author=get_logged_in_author())
        lb.from_name(username, owner, labbook_name)
        stop_labbook_monitor(lb, username)
        lb, stopped = ContainerOperations.stop_container(labbook=lb, username=username)

        if not stopped:
            raise ValueError(f"Failed to stop labbook {labbook_name}")

        return StopContainer(environment=Environment(owner=owner, name=labbook_name))
