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
from lmcommon.environment import ComponentRepository, get_package_manager
from lmcommon.labbook.schemas import CURRENT_SCHEMA
from lmcommon.gitlib.gitlab import GitLabManager

from lmsrvcore.auth.user import get_logged_in_username
from lmsrvcore.auth.identity import parse_token
from lmsrvcore.api.connections import ListBasedConnection

from lmsrvlabbook.api.objects.labbook import Labbook
from lmsrvlabbook.api.objects.remotelabbook import RemoteLabbook
from lmsrvlabbook.api.objects.basecomponent import BaseComponent
from lmsrvlabbook.api.objects.packagecomponent import PackageComponent
from lmsrvlabbook.api.objects.customcomponent import CustomComponent
from lmsrvlabbook.api.objects.jobstatus import JobStatus
from lmsrvlabbook.api.connections.labbook import LabbookConnection
from lmsrvlabbook.api.connections.remotelabbook import RemoteLabbookConnection
from lmsrvlabbook.api.connections.environment import BaseComponentConnection, CustomComponentConnection
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
    current_labbook_schema_version = graphene.Int()

    # Used to query for specific background jobs.
    # job_id is in the format of `rq:job:uuid`, though it should never need to be parsed.
    job_status = graphene.Field(JobStatus, job_id=graphene.String())

    # All background jobs in the system: Queued, Completed, Failed, and Started.
    background_jobs = graphene.relay.ConnectionField(JobStatusConnection)

    # Connection to locally available labbooks
    local_labbooks = graphene.relay.ConnectionField(LabbookConnection,
                                                    sort=graphene.String(default_value="az"),
                                                    reverse=graphene.Boolean(default_value=False))

    # Connection to remotely available labbooks
    remote_labbooks = graphene.relay.ConnectionField(RemoteLabbookConnection,
                                                     sort=graphene.String(default_value="az"),
                                                     reverse=graphene.Boolean(default_value=False))

    # Base Image Repository Interface
    available_bases = graphene.relay.ConnectionField(BaseComponentConnection)

    # Currently not fully supported, but will be added in the future.
    # available_base_image_versions = graphene.relay.ConnectionField(BaseImageConnection, repository=graphene.String(),
    #                                                                namespace=graphene.String(),
    #                                                                component=graphene.String())

    # Custom Dependency Repository Interface
    available_custom_dependencies = graphene.relay.ConnectionField(CustomComponentConnection)

    # Currently not fully supported, but will be added in the future.
    # available_custom_dependencies_versions = graphene.relay.ConnectionField(CustomDependencyConnection,
    #                                                                         repository=graphene.String(),
    #                                                                         namespace=graphene.String(),
    #                                                                         component=graphene.String())

    # Package Query for validating packages and getting latest versions
    package = graphene.Field(PackageComponent,
                             manager=graphene.String(),
                             package=graphene.String(),
                             version=graphene.String(default_value=""))

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
        """Return the current LabBook schema version"""
        return CURRENT_SCHEMA

    def resolve_job_status(self, info, job_id: str):
        """Method to return a graphene Labbok instance based on the name

        Uses the "currently logged in" user

        Args:
            job_id(dict): Contains user details

        Returns:
            JobStatus
        """
        return JobStatus(job_id)

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
            edge_objs.append(JobStatusConnection.Edge(node=JobStatus(edge), cursor=cursor))

        return JobStatusConnection(edges=edge_objs, page_info=lbc.page_info)

    def resolve_local_labbooks(self, info, sort: str, reverse: bool, **kwargs):
        """Method to return a all graphene Labbook instances for the logged in user

        Uses the "currently logged in" user

        Returns:
            list(Labbook)
        """
        lb = LabBook()

        username = get_logged_in_username()

        # Collect all labbooks for all owners
        edges = lb.list_local_labbooks(username=username, sort_mode=sort, reverse=reverse)
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]

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

    def resolve_remote_labbooks(self, info, sort: str, reverse: bool, **kwargs):
        """Method to return a all RemoteLabbook instances for the logged in user

        This is a remote call, so should be fetched on its own and only when needed. The user must have a valid
        session for data to be returned.

        It is recommended to use large page size (e.g. 50-100). This is due to how the remote server returns all the
        available data at once, so it is more efficient to load a lot of records at a time.

        Args:
            sort_mode(sort_mode): String specifying how labbooks should be sorted
            reverse(bool): Reverse sorting if True

        Supported sorting modes:
            - az: naturally sort
            - created_on: sort by creation date, newest first
            - modified_on: sort by modification date, newest first

        Returns:
            list(Labbook)
        """
        # Load config data
        configuration = Configuration().config

        # Extract valid Bearer token
        token = None
        if hasattr(info.context.headers, 'environ'):
            if "HTTP_AUTHORIZATION" in info.context.headers.environ:
                token = parse_token(info.context.headers.environ["HTTP_AUTHORIZATION"])
        if not token:
            raise ValueError("Authorization header not provided. Cannot list remote LabBooks.")

        # Get remote server configuration
        default_remote = configuration['git']['default_remote']
        admin_service = None
        for remote in configuration['git']['remotes']:
            if default_remote == remote:
                admin_service = configuration['git']['remotes'][remote]['admin_service']
                break

        if not admin_service:
            raise ValueError('admin_service could not be found')

        # Query backend for data
        mgr = GitLabManager(default_remote, admin_service, access_token=token)
        edges = mgr.list_labbooks(sort_mode=sort, reverse=reverse)
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, kwargs)
        lbc.apply()

        # Get Labbook instances
        edge_objs = []
        for edge, cursor in zip(lbc.edges, lbc.cursors):
            create_data = {"id": "{}&{}".format(edge["namespace"], edge["labbook_name"]),
                           "name": edge["labbook_name"],
                           "owner": edge["namespace"],
                           "description": edge["description"],
                           "creation_date_utc": edge["created_on"],
                           "modified_date_utc": edge["modified_on"]}

            edge_objs.append(RemoteLabbookConnection.Edge(node=RemoteLabbook(**create_data),
                                                          cursor=cursor))

        return RemoteLabbookConnection(edges=edge_objs, page_info=lbc.page_info)

    def resolve_available_bases(self, info, **kwargs):
        """Method to return a all graphene BaseImages that are available

        Returns:
            list(Labbook)
        """
        repo = ComponentRepository()
        edges = repo.get_component_list("base")
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, kwargs)
        lbc.apply()

        # Get BaseImage instances
        edge_objs = []
        for edge, cursor in zip(lbc.edges, lbc.cursors):
            edge_objs.append(BaseComponentConnection.Edge(node=BaseComponent(repository=edge['###repository###'],
                                                                             component_id=edge['id'],
                                                                             revision=int(edge['revision'])),
                                                          cursor=cursor))

        return BaseComponentConnection(edges=edge_objs, page_info=lbc.page_info)

    # Currently not fully supported, but will be added in the future.
    # def resolve_available_base_image_versions(self, info, repository, namespace, component, **kwargs):
    #     """Method to return a all graphene BaseImages that are available
    #
    #     Returns:
    #         list(Labbook)
    #     """
    #     repo = ComponentRepository()
    #     edges = repo.get_component_versions("base_image",
    #                                         repository,
    #                                         namespace,
    #                                         component)
    #     cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]
    #
    #     # Process slicing and cursor args
    #     lbc = ListBasedConnection(edges, cursors, kwargs)
    #     lbc.apply()
    #
    #     # Get BaseImage instances
    #     edge_objs = []
    #     for edge, cursor in zip(lbc.edges, lbc.cursors):
    #         id_data = {'component_data': edge[1],
    #                    'component_class': 'base_image',
    #                    'repo': repository,
    #                    'namespace': namespace,
    #                    'component': component,
    #                    'version': edge[0]
    #                    }
    #         edge_objs.append(BaseImageConnection.Edge(node=BaseImage.create(id_data), cursor=cursor))
    #
    #     return BaseImageConnection(edges=edge_objs, page_info=lbc.page_info)

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
            edge_objs.append(CustomComponentConnection.Edge(node=CustomComponent(repository=edge['###repository###'],
                                                                                 component_id=edge['id'],
                                                                                 revision=edge['revision']),
                                                            cursor=cursor))

        return CustomComponentConnection(edges=edge_objs, page_info=lbc.page_info)

    # Currently not fully supported, but will be added in the future.
    # def resolve_available_custom_dependencies_versions(self, info, repository, namespace, component, **kwargs):
    #     """Method to return all versions of a Custom Dependency component
    #
    #     Returns:
    #         CustomDependencyConnection
    #     """
    #     repo = ComponentRepository()
    #     edges = repo.get_component_versions("custom",
    #                                         repository,
    #                                         namespace,
    #                                         component)
    #     cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]
    #
    #     # Process slicing and cursor args
    #     lbc = ListBasedConnection(edges, cursors, kwargs)
    #     lbc.apply()
    #
    #     # Get BaseImage instances
    #     edge_objs = []
    #     for edge, cursor in zip(lbc.edges, lbc.cursors):
    #         id_data = {'component_data': edge[1],
    #                    'component_class': 'custom',
    #                    'repo': repository,
    #                    'namespace': namespace,
    #                    'component': component,
    #                    'version': edge[0]
    #                    }
    #         edge_objs.append(CustomDependencyConnection.Edge(node=CustomDependency.create(id_data), cursor=cursor))
    #
    #     return CustomDependencyConnection(edges=edge_objs, page_info=lbc.page_info)

    def resolve_user_identity(self, info):
        """Method to return a graphene UserIdentity instance based on the current logged (both on & offline) user

        Returns:
            UserIdentity
        """
        return UserIdentity()

    def resolve_package(self, info, manager, package, version):
        """Method to retrieve package component. Errors can be used to validate if a package name and version
        are correct

        Returns:
            PackageComponent
        """
        # Instantiate appropriate package manager
        mgr = get_package_manager(manager)

        # Validate package and version if available
        if version == "":
            version = None
        result = mgr.is_valid(package, version)

        if result.package is False:
            raise ValueError(f"Package name {package} is invalid")

        latest_version = None
        if not version:
            # If missing version, look up latest
            latest_version = mgr.latest_version(package)
            version = latest_version
        else:
            if result.version is False:
                # If version was set but is invalid, replace with latest
                latest_version = mgr.latest_version(package)
                version = latest_version

        # Return object
        return PackageComponent(manager=manager, package=package, version=version, latest_version=latest_version)
