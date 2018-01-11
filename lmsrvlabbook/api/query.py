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
import base64
from typing import List

import graphene

from lmcommon.labbook import LabBook
from lmcommon.logging import LMLogger
from lmcommon.configuration import Configuration
from lmcommon.dispatcher import Dispatcher
from lmcommon.environment import ComponentRepository

from lmsrvcore.auth.user import get_logged_in_username
from lmsrvcore.api.connections import ListBasedConnection

from lmsrvlabbook.api.objects.labbook import Labbook
from lmsrvlabbook.api.objects.baseimage import BaseImage
from lmsrvlabbook.api.objects.customdependency import CustomDependency
from lmsrvlabbook.api.objects.jobstatus import JobStatus
from lmsrvlabbook.api.connections.labbook import LabbookConnection
from lmsrvlabbook.api.connections.baseimage import BaseImageConnection
from lmsrvlabbook.api.connections.customdependency import CustomDependencyConnection
from lmsrvlabbook.api.connections.jobstatus import JobStatusConnection

from lmsrvcore.api.objects.user import UserIdentity


logger = LMLogger.get_logger()


class LabbookQuery(graphene.ObjectType):
    """Entry point for all LabBook queryable fields"""
    # Create instance of the LabBook dataloader for use across all objects within this query instance

    # Node Fields for Relay
    node = graphene.relay.Node.Field()

    build_info = graphene.String()

    labbook = graphene.Field(Labbook, owner=graphene.String(), name=graphene.String())

    # This indicates the most-recent labbook schema version.
    # Nominal usage of this field is to see if any given labbook is behind this version.
    # Any new labbook will be created with this schema version.
    current_labbook_schema_version = graphene.String()

    # Used to query for specific background jobs.
    # job_id is in the format of `rq:job:uuid`, though it should never need to be parsed.
    job_status = graphene.Field(JobStatus, job_id=graphene.String())

    # All background jobs in the system: Queued, Completed, Failed, and Started.
    background_jobs = graphene.relay.ConnectionField(JobStatusConnection)

    # Connection to locally available labbooks
    local_labbooks = graphene.relay.ConnectionField(LabbookConnection)

    # Base Image Repository Interface
    available_base_images = graphene.relay.ConnectionField(BaseImageConnection)
    available_base_image_versions = graphene.relay.ConnectionField(BaseImageConnection, repository=graphene.String(),
                                                                   namespace=graphene.String(),
                                                                   component=graphene.String())

    # Custom Dependency Repository Interface
    available_custom_dependencies = graphene.relay.ConnectionField(CustomDependencyConnection)
    available_custom_dependencies_versions = graphene.relay.ConnectionField(CustomDependencyConnection,
                                                                            repository=graphene.String(),
                                                                            namespace=graphene.String(),
                                                                            component=graphene.String())

    # Get the current logged in user identity, primarily used when running offline
    user_identity = graphene.Field(UserIdentity)

    def resolve_build_info(self, info):
        """Return this LabManager build info (hash, build timestamp, etc)"""
        build_info = Configuration().config.get('build_info') or {}
        return '-'.join([build_info.get('application', 'UnknownDate'),
                         build_info.get('revision', 'UnknownHash'),
                         build_info.get('built_on', 'UnknownApplication')])

    def resolve_labbook(self, info, owner: str, name: str):
        """Method to return a graphene Labbok instance based on the name

        Uses the "currently logged in" user

        Args:
            owner(str): Username of the owner (aka namespace)
            name(str): Name of the LabBook
            _dataloader: A dataloader instance

        Returns:
            Labbook
        """
        # Load the labbook data via a dataloader
        loader_key = f"{get_logged_in_username()}&{owner}&{name}"
        info.context.labbook_loader.load(loader_key)

        return Labbook(id="{}&{}".format(owner, name),
                       name=name, owner=owner)

    def resolve_current_labbook_schema_version(self, info):
        """Return the LabBook schema version (defined as static field in LabBook class."""
        return LabBook.LABBOOK_DATA_SCHEMA_VERSION

    def resolve_job_status(self, info, job_id: str):
        """Method to return a graphene Labbok instance based on the name

        Uses the "currently logged in" user

        Args:
            job_id(dict): Contains user details

        Returns:
            JobStatus
        """
        logger.info(f"Resolving jobStatus {job_id} (type {type(job_id)})")
        return JobStatus.create(job_id)

    def resolve_background_jobs(self, info, **kwargs):
        """Method to return a all background jobs the system is aware of: Queued, Started, Finished, Failed.

        Returns:
            list(JobStatus)
        """
        job_dispatcher = Dispatcher()

        edges: List[str] = [j.job_key.key_str for j in job_dispatcher.all_jobs]
        cursors = [base64.b64encode(f"{str(cnt)}".encode('utf-8')) for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, kwargs)
        lbc.apply()

        edge_objs = []
        for edge, cursor in zip(lbc.edges, lbc.cursors):
            edge_objs.append(JobStatusConnection.Edge(node=JobStatus.create(edge), cursor=cursor))

        return JobStatusConnection(edges=edge_objs, page_info=lbc.page_info)

    def resolve_local_labbooks(self, info, **kwargs):
        """Method to return a all graphene Labbook instances for the logged in user

        Uses the "currently logged in" user

        Returns:
            list(Labbook)
        """
        lb = LabBook()

        username = get_logged_in_username()
        labbooks = lb.list_local_labbooks(username=username)

        # Collect all labbooks for all owners
        edges = []
        cursors = []
        if labbooks:
            for key in labbooks.keys():
                edges.extend(labbooks[key])
            cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt,
                                                                                              x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, kwargs)
        lbc.apply()

        # Get Labbook instances
        edge_objs = []
        for edge, cursor in zip(lbc.edges, lbc.cursors):
            create_data = {"id": "{}&{}".format(edge["owner"], edge["name"]),
                           "name": edge["name"],
                           "owner": edge["owner"]}

            edge_objs.append(LabbookConnection.Edge(node=Labbook(**create_data),
                                                    cursor=cursor))

        return LabbookConnection(edges=edge_objs, page_info=lbc.page_info)

    def resolve_available_base_images(self, info, **kwargs):
        """Method to return a all graphene BaseImages that are available

        Returns:
            list(Labbook)
        """
        repo = ComponentRepository()
        edges = repo.get_component_list("base_image")
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, kwargs)
        lbc.apply()

        # Get BaseImage instances
        edge_objs = []
        for edge, cursor in zip(lbc.edges, lbc.cursors):
            id_data = {'component_data': edge,
                       'component_class': 'base_image',
                       'repo': edge['###repository###'],
                       'namespace': edge['###namespace###'],
                       'component': edge['info']['name'],
                       'version': "{}.{}".format(edge['info']['version_major'], edge['info']['version_minor'])
                       }
            edge_objs.append(BaseImageConnection.Edge(node=BaseImage.create(id_data), cursor=cursor))

        return BaseImageConnection(edges=edge_objs, page_info=lbc.page_info)

    def resolve_available_base_image_versions(self, info, repository, namespace, component, **kwargs):
        """Method to return a all graphene BaseImages that are available

        Returns:
            list(Labbook)
        """
        repo = ComponentRepository()
        edges = repo.get_component_versions("base_image",
                                            repository,
                                            namespace,
                                            component)
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, kwargs)
        lbc.apply()

        # Get BaseImage instances
        edge_objs = []
        for edge, cursor in zip(lbc.edges, lbc.cursors):
            id_data = {'component_data': edge[1],
                       'component_class': 'base_image',
                       'repo': repository,
                       'namespace': namespace,
                       'component': component,
                       'version': edge[0]
                       }
            edge_objs.append(BaseImageConnection.Edge(node=BaseImage.create(id_data), cursor=cursor))

        return BaseImageConnection(edges=edge_objs, page_info=lbc.page_info)

    def resolve_available_custom_dependencies(self, info, **kwargs):
        """Method to return all graphene CustomDependencies that are available (at the latest version)

        Returns:
            CustomDependencyConnection
        """
        repo = ComponentRepository()
        edges = repo.get_component_list("custom")
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, kwargs)
        lbc.apply()

        # Get BaseImage instances
        edge_objs = []
        for edge, cursor in zip(lbc.edges, lbc.cursors):
            id_data = {'component_data': edge,
                       'component_class': 'custom',
                       'repo': edge['###repository###'],
                       'namespace': edge['###namespace###'],
                       'component': edge['info']['name'],
                       'version': "{}.{}".format(edge['info']['version_major'], edge['info']['version_minor'])
                       }
            edge_objs.append(CustomDependencyConnection.Edge(node=CustomDependency.create(id_data), cursor=cursor))

        return CustomDependencyConnection(edges=edge_objs, page_info=lbc.page_info)

    def resolve_available_custom_dependencies_versions(self, info, repository, namespace, component, **kwargs):
        """Method to return all versions of a Custom Dependency component

        Returns:
            CustomDependencyConnection
        """
        repo = ComponentRepository()
        edges = repo.get_component_versions("custom",
                                            repository,
                                            namespace,
                                            component)
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, kwargs)
        lbc.apply()

        # Get BaseImage instances
        edge_objs = []
        for edge, cursor in zip(lbc.edges, lbc.cursors):
            id_data = {'component_data': edge[1],
                       'component_class': 'custom',
                       'repo': repository,
                       'namespace': namespace,
                       'component': component,
                       'version': edge[0]
                       }
            edge_objs.append(CustomDependencyConnection.Edge(node=CustomDependency.create(id_data), cursor=cursor))

        return CustomDependencyConnection(edges=edge_objs, page_info=lbc.page_info)

    def resolve_user_identity(self, info):
        """Method to return a graphene UserIdentity instance based on the current logged (both on & offline) user

        Returns:
            UserIdentity
        """
        return UserIdentity()
