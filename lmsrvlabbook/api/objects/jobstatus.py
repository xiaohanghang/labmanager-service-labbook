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

from lmcommon.logging import LMLogger
from lmcommon.dispatcher import Dispatcher, JobKey

from lmsrvcore.api import logged_query

logger = LMLogger.get_logger()


class JobStatus(graphene.ObjectType):
    """A query to get the status of a background task launched with the Dispatcher"""

    class Meta:
        interfaces = (graphene.relay.Node,)

    # The Dispatcher returns a unique opaque id of the background job.
    job_key = graphene.Field(graphene.String)

    # Status is either: queued, failed, started, finished.
    status = graphene.Field(graphene.String)

    # Message if job has failed, if not in failed state this is None/null.
    failure_message = graphene.String()

    # Timestamp the task was put into the queue
    started_at = graphene.Field(graphene.String)

    # Timestamp the task was regarded as either failed or finished.
    finished_at = graphene.Field(graphene.String)

    # Result.. None if no result or void method.
    result = graphene.Field(graphene.String)

    @staticmethod
    def to_type_id(id_data):
        """Method to generate a single string that uniquely identifies this object

        Args:
            id_data(dict):

        Returns:
            str
        """
        return "{}".format(id_data["job_id"])

    @staticmethod
    def parse_type_id(type_id):
        """Method to parse an ID for a given type into its identifiable variables returned as a dictionary of strings

        Args:
            type_id (str): type unique identifier

        Returns:
            dict
        """
        return {"job_id": type_id}

    @staticmethod
    @logged_query
    def create(job_id: str):
        """Method to retrieve status info for given background job.

        Args:
            job_id(str): Unique key of the background job.

        Returns:
            JobStatus
        """
        d = Dispatcher()
        task_ref = d.query_task(JobKey(job_id))
        logger.info(f'Retrieved reference {str(task_ref)} for job_id `{job_id}`')
        js = JobStatus(job_key=task_ref.job_key.key_str,
                       status=task_ref.status,
                       started_at=task_ref.started_at,
                       finished_at=task_ref.finished_at,
                       result=task_ref.result,
                       failure_message=task_ref.failure_message)
        return js
