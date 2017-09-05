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
    """A type that represents a Development Environment Environment Component"""

    class Meta:
        interfaces = (graphene.relay.Node,)

    status = graphene.Field(graphene.String)
    started_at = graphene.Field(graphene.String)
    finished_at = graphene.Field(graphene.String)
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
    def create(id_data):
        """Method to create a graphene JobStatus object based on the type node ID or id_data

        Args:
            id_data(dict):

        Returns:
            DevEnv
        """
        if "type_id" in id_data:
            # Parse ID components
            id_data.update(JobStatus.parse_type_id(id_data["type_id"]))
            del id_data["type_id"]

        d = Dispatcher()

        logger.info('Retrieving query for JobStatus on task_id `{}`...'.format(id_data['job_id']))
        job_ref = d.query_task(id_data['job_id'])
        logger.info('Retrieved reference {} for task_id `{}`'.format(str(job_ref), id_data['job_id']))

        return JobStatus(status=job_ref.get('status'),
                         started_at=job_ref.get('started_at'),
                         finished_at=job_ref.get('ended_at'),
                         result=job_ref.get('result'))
