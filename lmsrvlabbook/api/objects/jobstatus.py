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

from lmcommon.logging import LMLogger
from lmcommon.dispatcher import Dispatcher, JobKey


logger = LMLogger.get_logger()


class JobStatus(graphene.ObjectType, interface=(graphene.relay.Node,)):
    """A query to get the status of a background task launched with the Dispatcher"""

    # The Dispatcher returns a unique opaque id of the background job.
    job_key = graphene.Field(graphene.String)

    # Status is either: queued, failed, started, finished.
    status = graphene.Field(graphene.String)

    # Job desciption/metadata
    job_metadata = graphene.String()

    # Message if job has failed, if not in failed state this is None/null.
    failure_message = graphene.String()

    # Timestamp the task was put into the queue
    started_at = graphene.Field(graphene.String)

    # Timestamp the task was regarded as either failed or finished.
    finished_at = graphene.Field(graphene.String)

    # Result.. None if no result or void method.
    result = graphene.Field(graphene.String)

    @classmethod
    def get_node(cls, info, id):
        """Method to resolve the object based on it's Node ID"""
        # Parse the key
        d = Dispatcher()
        status = d.query_task(JobKey(id))
        return JobStatus(job_key=status.job_key.key_str,
                         status=status.status,
                         started_at=status.started_at,
                         finished_at=status.finished_at,
                         job_metadata=status.meta,
                         result=status.result,
                         failure_message=status.failure_message)

    def resolve_id(self, info):
        if not self.id:
            if not self.job_key:
                raise ValueError("Resolving a JobStatus Node ID requires job_key to be set")
            self.id = self.job_key
        return self.id
