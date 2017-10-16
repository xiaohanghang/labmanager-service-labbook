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
from typing import List

import graphene
from graphene import resolve_only_args

from lmcommon.labbook import LabBook
from lmcommon.logging import LMLogger
from lmcommon.dispatcher import Dispatcher
from lmcommon.environment import ComponentRepository

from lmsrvcore.auth.user import get_logged_in_username
from lmsrvcore.api.connections import ListBasedConnection

from lmsrvlabbook.api.objects.labbook import Labbook
from lmsrvlabbook.api.objects.baseimage import BaseImage
from lmsrvlabbook.api.objects.devenv import DevEnv
from lmsrvlabbook.api.objects.customdependency import CustomDependency
from lmsrvlabbook.api.objects.jobstatus import JobStatus
from lmsrvlabbook.api.connections.labbook import LabbookConnection
from lmsrvlabbook.api.connections.baseimage import BaseImageConnection
from lmsrvlabbook.api.connections.devenv import DevEnvConnection
from lmsrvlabbook.api.connections.customdependency import CustomDependencyConnection
from lmsrvlabbook.api.connections.jobstatus import JobStatusConnection

logger = LMLogger.get_logger()


class LabbookQuery(graphene.AbstractType):
    """Entry point for all LabBook queryable fields"""
    # Node Fields for Relay
    node = graphene.relay.Node.Field()

    labbook = graphene.Field(Labbook, owner=graphene.String(), name=graphene.String())

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
    # Development Environment Repository Interface
    available_dev_envs = graphene.relay.ConnectionField(DevEnvConnection)
    available_dev_env_versions = graphene.relay.ConnectionField(DevEnvConnection, repository=graphene.String(),
                                                                namespace=graphene.String(),
                                                                component=graphene.String())
    # Custom Dependency Repository Interface
    available_custom_dependencies = graphene.relay.ConnectionField(CustomDependencyConnection)
    available_custom_dependencies_versions = graphene.relay.ConnectionField(CustomDependencyConnection,
                                                                            repository=graphene.String(),
                                                                            namespace=graphene.String(),
                                                                            component=graphene.String())

    def resolve_labbook(self, args, context, info):
        """Method to return a graphene Labbok instance based on the name

        Uses the "currently logged in" user

        Args:
            owner(dict): Contains user details
            name(str): Name of the LabBook

        Returns:
            Labbook
        """
        id_data = {"name": args.get('name'), "owner": args.get('owner')}
        return Labbook.create(id_data)

    @resolve_only_args
    def resolve_job_status(self, job_id: str):
        """Method to return a graphene Labbok instance based on the name

        Uses the "currently logged in" user

        Args:
            job_id(dict): Contains user details

        Returns:
            JobStatus
        """
        logger.info(f"Resolving jobStatus {job_id} (type {type(job_id)})")
        return JobStatus.create(job_id)

    def resolve_background_jobs(self, args, context, info):
        """Method to return a all background jobs the system is aware of: Queued, Started, Finished, Failed.

        Returns:
            list(JobStatus)
        """
        job_dispatcher = Dispatcher()

        edges: List[str] = [j.job_key.key_str for j in job_dispatcher.all_jobs]
        cursors = [base64.b64encode(f"{str(cnt)}".encode('utf-8')) for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, args)
        lbc.apply()

        edge_objs = []
        for edge, cursor in zip(lbc.edges, lbc.cursors):
            edge_objs.append(JobStatusConnection.Edge(node=JobStatus.create(edge), cursor=cursor))

        return JobStatusConnection(edges=edge_objs, page_info=lbc.page_info)

    def resolve_local_labbooks(self, args, context, info):
        """Method to return a all graphene Labbook instances for the logged in user

        Uses the "currently logged in" user

        Returns:
            list(Labbook)
        """
        lb = LabBook()

        # TODO: Lookup name based on logged in user when available
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
        lbc = ListBasedConnection(edges, cursors, args)
        lbc.apply()

        # Get Labbook instances
        id_data = {"username": username}
        edge_objs = []
        for edge, cursor in zip(lbc.edges, lbc.cursors):
            id_data["name"] = edge["name"]
            id_data["owner"] = edge["owner"]
            edge_objs.append(LabbookConnection.Edge(node=Labbook.create(id_data), cursor=cursor))

        return LabbookConnection(edges=edge_objs, page_info=lbc.page_info)

    def resolve_available_base_images(self, args, context, info):
        """Method to return a all graphene BaseImages that are available

        Returns:
            list(Labbook)
        """
        repo = ComponentRepository()
        edges = repo.get_component_list("base_image")
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, args)
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

    def resolve_available_base_image_versions(self, args, context, info):
        """Method to return a all graphene BaseImages that are available

        Returns:
            list(Labbook)
        """
        repo = ComponentRepository()
        edges = repo.get_component_versions("base_image",
                                            args['repository'],
                                            args['namespace'],
                                            args['component'])
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, args)
        lbc.apply()

        # Get BaseImage instances
        edge_objs = []
        for edge, cursor in zip(lbc.edges, lbc.cursors):
            id_data = {'component_data': edge[1],
                       'component_class': 'base_image',
                       'repo': args['repository'],
                       'namespace': args['namespace'],
                       'component': args['component'],
                       'version': edge[0]
                       }
            edge_objs.append(BaseImageConnection.Edge(node=BaseImage.create(id_data), cursor=cursor))

        return BaseImageConnection(edges=edge_objs, page_info=lbc.page_info)

    def resolve_available_dev_envs(self, args, context, info):
        """Method to return all graphene DevEnvs that are available (at the latest version)

        Returns:
            DevEnvConnection
        """
        repo = ComponentRepository()
        edges = repo.get_component_list("dev_env")
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, args)
        lbc.apply()

        # Get BaseImage instances
        edge_objs = []
        for edge, cursor in zip(lbc.edges, lbc.cursors):
            id_data = {'component_data': edge,
                       'component_class': 'dev_env',
                       'repo': edge['###repository###'],
                       'namespace': edge['###namespace###'],
                       'component': edge['info']['name'],
                       'version': "{}.{}".format(edge['info']['version_major'], edge['info']['version_minor'])
                       }
            edge_objs.append(DevEnvConnection.Edge(node=DevEnv.create(id_data), cursor=cursor))

        return DevEnvConnection(edges=edge_objs, page_info=lbc.page_info)

    def resolve_available_dev_env_versions(self, args, context, info):
        """Method to return all versions of a Dev Env component

        Returns:
            DevEnvConnection
        """
        repo = ComponentRepository()
        edges = repo.get_component_versions("dev_env",
                                            args['repository'],
                                            args['namespace'],
                                            args['component'])
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, args)
        lbc.apply()

        # Get BaseImage instances
        edge_objs = []
        for edge, cursor in zip(lbc.edges, lbc.cursors):
            id_data = {'component_data': edge[1],
                       'component_class': 'dev_env',
                       'repo': args['repository'],
                       'namespace': args['namespace'],
                       'component': args['component'],
                       'version': edge[0]
                       }
            edge_objs.append(DevEnvConnection.Edge(node=DevEnv.create(id_data), cursor=cursor))

        return DevEnvConnection(edges=edge_objs, page_info=lbc.page_info)

    def resolve_available_custom_dependencies(self, args, context, info):
        """Method to return all graphene CustomDependencies that are available (at the latest version)

        Returns:
            CustomDependencyConnection
        """
        repo = ComponentRepository()
        edges = repo.get_component_list("custom")
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, args)
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

    def resolve_available_custom_dependencies_versions(self, args, context, info):
        """Method to return all versions of a Custom Dependency component

        Returns:
            CustomDependencyConnection
        """
        repo = ComponentRepository()
        edges = repo.get_component_versions("custom",
                                            args['repository'],
                                            args['namespace'],
                                            args['component'])
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, args)
        lbc.apply()

        # Get BaseImage instances
        edge_objs = []
        for edge, cursor in zip(lbc.edges, lbc.cursors):
            id_data = {'component_data': edge[1],
                       'component_class': 'custom',
                       'repo': args['repository'],
                       'namespace': args['namespace'],
                       'component': args['component'],
                       'version': edge[0]
                       }
            edge_objs.append(CustomDependencyConnection.Edge(node=CustomDependency.create(id_data), cursor=cursor))

        return CustomDependencyConnection(edges=edge_objs, page_info=lbc.page_info)
