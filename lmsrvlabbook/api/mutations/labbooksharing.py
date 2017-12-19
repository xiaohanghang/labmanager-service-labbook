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
import base64
import os
from docker.errors import ImageNotFound

import graphene

from lmcommon.configuration import Configuration, get_docker_client
from lmcommon.dispatcher import (Dispatcher, jobs)
from lmcommon.labbook import LabBook
from lmcommon.logging import LMLogger
from lmcommon.imagebuilder import ImageBuilder
from lmcommon.activity import ActivityStore, ActivityDetailRecord, ActivityDetailType, ActivityRecord, ActivityType

from lmsrvcore.api import logged_mutation
from lmsrvcore.api.mutations import ChunkUploadMutation, ChunkUploadInput
from lmsrvcore.auth.identity import parse_token
from lmsrvcore.auth.user import get_logged_in_username
from lmsrvlabbook.api.connections.labbookfileconnection import LabbookFavoriteConnection
from lmsrvlabbook.api.connections.labbookfileconnection import LabbookFileConnection
from lmsrvlabbook.api.objects.labbook import Labbook
from lmsrvlabbook.api.objects.labbookfile import LabbookFavorite, LabbookFile

logger = LMLogger.get_logger()


class PublishLabbook(graphene.relay.ClientIDMutation):

    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)

    success = graphene.Boolean()

    @classmethod
    @logged_mutation
    def mutate_and_get_payload(cls, input, context, info):
        # Load LabBook
        username = get_logged_in_username()
        working_directory = Configuration().config['git']['working_directory']
        inferred_lb_directory = os.path.join(working_directory, username, input['owner'], 'labbooks',
                                             input['labbook_name'])
        lb = LabBook()
        lb.from_directory(inferred_lb_directory)

        # Extract valid Bearer token
        if "HTTP_AUTHORIZATION" in context.headers.environ:
            token = parse_token(context.headers.environ["HTTP_AUTHORIZATION"])
        else:
            raise ValueError("Authorization header not provided. Must have a valid session to query for collaborators")

        # BVB -- Should this defer to `sync` if Labbook's remote is already set?
        # Otherwise, it will throw an exception, which may still be ok.
        lb.publish(username=username, access_token=token)

        return PublishLabbook(success=True)


class SyncLabbook(graphene.relay.ClientIDMutation):

    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)

    # How many upstream commits it pulled in.
    update_count = graphene.Int()

    @classmethod
    @logged_mutation
    def mutate_and_get_payload(cls, input, context, info):
        # Load LabBook
        username = get_logged_in_username()
        working_directory = Configuration().config['git']['working_directory']
        inferred_lb_directory = os.path.join(working_directory, username, input['owner'], 'labbooks',
                                             input['labbook_name'])
        lb = LabBook()
        lb.from_directory(inferred_lb_directory)
        cnt = lb.sync(username=username)

        return SyncLabbook(update_count=cnt)
