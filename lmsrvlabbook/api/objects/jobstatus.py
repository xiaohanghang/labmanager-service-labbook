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
from lmcommon.dispatcher import Dispatcher

from lmsrvcore.api import ObjectType

logger = LMLogger.get_logger()


class JobStatus(ObjectType):
    """A query to get the status of a background task launched with the Dispatcher"""

    class Meta:
        interfaces = (graphene.relay.Node,)

    # The Dispatcher returns a unique opaque id of the background job.
    job_key = graphene.Field(graphene.String)

    # Status is either: queued, failed, started, finished.
    status = graphene.Field(graphene.String)

    # Timestamp the task was put into the queue
    started_at = graphene.Field(graphene.String)

    # Timestampo the task was regarded as either failed or finished.
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
    def create(job_id):
        """Method to retrieve status info for given background job.

        Args:
            job_id(str): Unique key of the background job.

        Returns:
            JobStatus
        """
        logger.info('Retrieving query for JobStatus on task_id `{}`...'.format(job_id))
        logger.info('Note: {} decoded is {}'.format(job_id, job_id.encode()))
        d = Dispatcher()

        job_ref = d.query_task(job_id)
        logger.info('Retrieved reference {} for job_id `{}`'.format(str(job_ref), job_id))

        return JobStatus(job_key=job_id,
                         status=job_ref.get('status'),
                         started_at=job_ref.get('started_at'),
                         finished_at=job_ref.get('ended_at'),
                         result=job_ref.get('result'))
