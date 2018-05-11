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
import graphene

from lmcommon.logging import LMLogger
from lmcommon.dispatcher import Dispatcher
from lmcommon.workflows import BranchManager
from lmcommon.activity import ActivityStore
from lmcommon.gitlib.gitlab import GitLabManager
from lmcommon.files import FileOperations
from lmcommon.environment import get_package_manager

from lmsrvcore.auth.user import get_logged_in_username

from lmsrvcore.api.connections import ListBasedConnection
from lmsrvcore.api.interfaces import GitRepository
from lmsrvcore.auth.identity import parse_token


from lmsrvlabbook.api.objects.jobstatus import JobStatus
from lmsrvlabbook.api.connections.ref import LabbookRefConnection
from lmsrvlabbook.api.objects.environment import Environment
from lmsrvlabbook.api.objects.overview import LabbookOverview
from lmsrvlabbook.api.objects.ref import LabbookRef
from lmsrvlabbook.api.objects.labbooksection import LabbookSection
from lmsrvlabbook.api.connections.activity import ActivityConnection
from lmsrvlabbook.api.objects.activity import ActivityDetailObject, ActivityRecordObject
from lmsrvlabbook.api.objects.packagecomponent import PackageComponent

logger = LMLogger.get_logger()


class Labbook(graphene.ObjectType, interfaces=(graphene.relay.Node, GitRepository)):
    """A type representing a LabBook and all of its contents

    LabBooks are uniquely identified by both the "owner" and the "name" of the LabBook

    """
    # Store collaborator data so it is only fetched once per request
    _collaborators = None

    # A short description of the LabBook limited to 140 UTF-8 characters
    description = graphene.String()

    # An arbitrarily long markdown document
    readme = graphene.String()

    # Data schema version of this labbook. It may be behind the most recent version and need
    # to be upgraded.
    schema_version = graphene.Int()

    # Size on disk of LabBook in bytes
    # NOTE: This is a string since graphene can't represent ints bigger than 2**32
    size_bytes = graphene.String()

    # Name of currently active (checked-out) branch
    active_branch_name = graphene.String()

    # Primary user branch of repo (known also as "Workspace Branch" or "trunk")
    workspace_branch_name = graphene.String()

    # All available feature/rollback branches (Collectively known as experimental branches)
    available_branch_names = graphene.List(graphene.String)

    # Names of branches that can be merged into the current active branch
    mergeable_branch_names = graphene.List(graphene.String)

    # The name of the current branch
    # NOTE: DEPRECATED
    active_branch = graphene.Field(LabbookRef, deprecation_reason="Can use workspaceBranchName instead")

    # List of branches
    # NOTE: DEPRECATED
    branches = graphene.relay.ConnectionField(LabbookRefConnection,
                                              deprecation_reason="Can use availableBranchNames instead")

    # Get the URL of the remote origin
    default_remote = graphene.String()

    # Creation date/timestamp in UTC in ISO format
    creation_date_utc = graphene.types.datetime.DateTime()

    # List of collaborators
    collaborators = graphene.List(graphene.String)

    # A boolean indicating if the current user can manage collaborators
    can_manage_collaborators = graphene.Boolean()

    # How many commits the current active_branch is behind remote (0 if up-to-date or local-only).
    updates_available_count = graphene.Int()

    # Whether repo state is clean
    is_repo_clean = graphene.Boolean()

    # Environment Information
    environment = graphene.Field(Environment)

    # Overview Information
    overview = graphene.Field(LabbookOverview)

    # List of sections
    code = graphene.Field(LabbookSection)
    input = graphene.Field(LabbookSection)
    output = graphene.Field(LabbookSection)

    # Connection to Activity Entries
    activity_records = graphene.relay.ConnectionField(ActivityConnection)

    # Access a detail record directly, which is useful when fetching detail items
    detail_record = graphene.Field(ActivityDetailObject, key=graphene.String())
    detail_records = graphene.List(ActivityDetailObject, keys=graphene.List(graphene.String))

    # List of keys of all background jobs pertaining to this labbook (queued, started, failed, etc.)
    background_jobs = graphene.List(JobStatus)

    # Package Query for validating packages and getting latest versions
    package = graphene.Field(PackageComponent,
                             manager=graphene.String(),
                             package=graphene.String(),
                             version=graphene.String(default_value=""))

    def _fetch_collaborators(self, info):
        """Helper method to fetch this labbook's collaborators

        Args:
            info: The graphene info object for this requests

        """
        lb = info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").get()

        # TODO: Future work will look up remote in LabBook data, allowing user to select remote.
        default_remote = lb.labmanager_config.config['git']['default_remote']
        admin_service = None
        for remote in lb.labmanager_config.config['git']['remotes']:
            if default_remote == remote:
                admin_service = lb.labmanager_config.config['git']['remotes'][remote]['admin_service']
                break

        # Extract valid Bearer token
        if "HTTP_AUTHORIZATION" in info.context.headers.environ:
            token = parse_token(info.context.headers.environ["HTTP_AUTHORIZATION"])
        else:
            raise ValueError("Authorization header not provided. Must have a valid session to query for collaborators")

        # Get collaborators from remote service
        mgr = GitLabManager(default_remote, admin_service, token)
        try:
            self._collaborators = mgr.get_collaborators(self.owner, self.name)
        except ValueError:
            # If ValueError Raised, assume repo doesn't exist yet
            self._collaborators = []

    @classmethod
    def get_node(cls, info, id):
        """Method to resolve the object based on it's Node ID"""
        # Parse the key
        owner, name = id.split("&")

        return Labbook(id="{}&{}".format(owner, name),
                       name=name, owner=owner)

    def resolve_id(self, info):
        """Resolve the unique Node id for this object"""
        if not self.id:
            if not self.owner or not self.name:
                raise ValueError("Resolving a Labbook Node ID requires owner and name to be set")
            self.id = f"{self.owner}&{self.name}"

        return self.id

    def resolve_description(self, info):
        """Get number of commits the active_branch is behind its remote counterpart.
        Returns 0 if up-to-date or if local only."""
        if not self.description:
            lb = info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").get()
            self.description = lb.description

        return self.description

    def resolve_readme(self, info):
        """Resolve the readme document inside the labbook"""
        if not self.readme:
            lb = info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").get()
            self.readme = lb.get_readme()

        return self.readme

    def resolve_environment(self, info):
        """"""
        return Environment(id=f"{self.owner}&{self.name}", owner=self.owner, name=self.name)

    def resolve_overview(self, info):
        """"""
        return LabbookOverview(id=f"{self.owner}&{self.name}", owner=self.owner, name=self.name)

    def resolve_schema_version(self, info):
        """Get number of commits the active_branch is behind its remote counterpart.
        Returns 0 if up-to-date or if local only."""
        lb = info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").get()
        return lb.schema

    def resolve_size_bytes(self, info):
        """Return the size of the labbook on disk (in bytes).
        NOTE! This must be a string, as graphene can't quite handle big integers. """
        lb = info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").get()
        return str(FileOperations.content_size(labbook=lb))

    def resolve_updates_available_count(self, info):
        """Get number of commits the active_branch is behind its remote counterpart.
        Returns 0 if up-to-date or if local only."""
        lb = info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").get()

        # Note, by default using remote "origin"
        return lb.get_commits_behind_remote("origin")[1]

    def resolve_active_branch_name(self, info):
        lb = info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").get()
        bm = BranchManager(labbook=lb, username=get_logged_in_username())
        return bm.active_branch

    def resolve_workspace_branch_name(self, info):
        lb = info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").get()
        bm = BranchManager(labbook=lb, username=get_logged_in_username())
        return bm.workspace_branch

    def resolve_available_branch_names(self, info):
        lb = info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").get()
        bm = BranchManager(labbook=lb, username=get_logged_in_username())
        return bm.branches

    def resolve_mergeable_branch_names(self, info):
        lb = info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").get()
        bm = BranchManager(labbook=lb, username=get_logged_in_username())
        return bm.mergeable_branches

    def resolve_active_branch(self, info):
        """Method to get the active branch

        Args:
            args:
            context:
            info:

        Returns:

        """
        lb = info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").get()
        ref_name = lb.git.get_current_branch_name()

        return LabbookRef(id=f"{self.owner}&{self.name}&None&{ref_name}",
                          owner=self.owner, name=self.name, prefix=None,
                          ref_name=ref_name)

    def resolve_is_repo_clean(self, info):
        """Return True if no untracked files and no uncommitted changes (i.e., Git repo clean)

        Args:
            args:
            context:
            info:

        Returns:

        """
        lb = info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").get()
        return lb.is_repo_clean

    def resolve_creation_date_utc(self, info):
        """Return the creation timestamp (if available - otherwise empty string)

        Args:
            args:
            context:
            info:

        Returns:

        """
        lb = info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").get()
        # Note! creation_date might be None!!
        return lb.creation_date

    def resolve_default_remote(self, info):
        """Return True if no untracked files and no uncommitted changes (i.e., Git repo clean)

        Args:
            args:
            context:
            info:

        Returns:

        """
        lb = info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").get()
        remotes = lb.git.list_remotes()
        if remotes:
            url = [x['url'] for x in remotes if x['name'] == 'origin']
            if url:
                return url[0]
            else:
                logger.warning(f"There exist remotes in {str(lb)}, but no origin found.")
        return None

    def resolve_branches(self, info, **kwargs):
        """Method to page through branch Refs

        Args:
            args:
            context:
            info:

        Returns:

        """
        lb = info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").get()

        # Get all edges and cursors. Here, cursors are just an index into the refs
        edges = [x for x in lb.git.repo.refs]
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt,
                                                                                          x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, kwargs)
        lbc.apply()

        # Get LabbookRef instances
        edge_objs = []
        for edge, cursor in zip(lbc.edges, lbc.cursors):
            parts = edge.name.split("/")
            if len(parts) > 1:
                prefix = parts[0]
                branch = parts[1]
            else:
                prefix = None
                branch = parts[0]

            create_data = {"name": lb.name,
                           "owner": self.owner,
                           "prefix": prefix,
                           "ref_name": branch}
            edge_objs.append(LabbookRefConnection.Edge(node=LabbookRef(**create_data), cursor=cursor))

        return LabbookRefConnection(edges=edge_objs,
                                    page_info=lbc.page_info)

    def resolve_code(self, info):
        """Method to resolve the code section"""
        return LabbookSection(id="{}&{}&{}".format(self.owner, self.name, 'code'),
                              owner=self.owner, name=self.name, section='code')

    def resolve_input(self, info):
        """Method to resolve the input section"""
        return LabbookSection(id="{}&{}&{}".format(self.owner, self.name, 'input'),
                              owner=self.owner, name=self.name, section='input')

    def resolve_output(self, info):
        """Method to resolve the output section"""
        return LabbookSection(id="{}&{}&{}".format(self.owner, self.name, 'output'),
                              owner=self.owner, name=self.name, section='output')

    def resolve_activity_records(self, info, **kwargs):
        """Method to page through branch Refs

        Args:
            kwargs:
            info:

        Returns:

        """
        lb = info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").get()

        # Create instance of ActivityStore for this LabBook
        store = ActivityStore(lb)

        if kwargs.get('before') or kwargs.get('last'):
            raise ValueError("Only `after` and `first` arguments are supported when paging activity records")

        # Get edges and cursors
        edges = store.get_activity_records(after=kwargs.get('after'), first=kwargs.get('first'))
        if edges:
            cursors = [x.commit for x in edges]
        else:
            cursors = []

        # Get ActivityRecordObject instances
        edge_objs = []
        for edge, cursor in zip(edges, cursors):
            edge_objs.append(ActivityConnection.Edge(node=ActivityRecordObject(id=f"{self.owner}&{self.name}&{edge.commit}",
                                                                               owner=self.owner,
                                                                               name=self.name,
                                                                               commit=edge.commit,
                                                                               _activity_record=edge),
                                                     cursor=cursor))

        # Create page info based on first commit. Since only paging backwards right now, just check for commit
        if edges:
            has_next_page = True

            # Get the message of the linked commit and check if it is the non-activity record labbook creation commit
            if edges[-1].linked_commit != "no-linked-commit":
                linked_msg = lb.git.log_entry(edges[-1].linked_commit)['message']
                if linked_msg == f"Creating new empty LabBook: {lb.name}" and "_GTM_ACTIVITY_" not in linked_msg:
                    # if you get here, this is the first activity record
                    has_next_page = False

            end_cursor = cursors[-1]
        else:
            has_next_page = False
            end_cursor = None

        page_info = graphene.relay.PageInfo(has_next_page=has_next_page, has_previous_page=False, end_cursor=end_cursor)

        return ActivityConnection(edges=edge_objs, page_info=page_info)

    def resolve_detail_record(self, info, key):
        """Method to resolve the detail record object

        Args:
            args:
            info:

        Returns:

        """
        return ActivityDetailObject(id=f"{self.owner}&{self.name}&{key}",
                                    owner=self.owner,
                                    name=self.name,
                                    key=key)

    def resolve_detail_records(self, info, keys):
        """Method to resolve multiple detail record objects

        Args:
            args:
            info:

        Returns:

        """
        return [ActivityDetailObject(id=f"{self.owner}&{self.name}&{key}",
                                     owner=self.owner,
                                     name=self.name,
                                     key=key) for key in keys]

    def resolve_collaborators(self, info):
        """Method to get the list of collaborators for a labbook

        Args:
            info:

        Returns:

        """
        if self._collaborators is None:
            self._fetch_collaborators(info)

        return [x[1] for x in self._collaborators]

    def resolve_can_manage_collaborators(self, info):
        """Method to check if the user is the "owner" of the labbook and can manage collaborators

        Args:
            info:

        Returns:

        """
        if self._collaborators is None:
            self._fetch_collaborators(info)

        can_manage = False
        username = get_logged_in_username()
        for c in self._collaborators:
            if c[1] == username:
                if c[2] is True:
                    can_manage = True

        return can_manage

    def resolve_background_jobs(self, info):
        """ Return the job keys, tasks, and statuses for all background jobs. """
        lb = info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").get()

        d = Dispatcher()
        jobs = d.get_jobs_for_labbook(labbook_key=lb.key)
        return [JobStatus(j.job_key.key_str) for j in jobs]

    def resolve_package(self, info, manager, package, version):
        """Method to retrieve package component. Errors can be used to validate if a package name and version
        are correct

        Returns:
            PackageComponent
        """
        lb = info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").get()

        # Instantiate appropriate package manager
        mgr = get_package_manager(manager)

        # Validate package and version if available
        if version == "":
            version = None
        result = mgr.is_valid(package, lb, get_logged_in_username(), package_version=version)
        if result.package is False:
            raise ValueError(f"Package name {package} is invalid")

        latest_version = mgr.latest_version(package, lb, get_logged_in_username())
        if not version:
            # If missing version, look up latest
            latest_version = mgr.latest_version(package, lb, get_logged_in_username())
            version = latest_version
        else:
            if result.version is False:
                # If version was set but is invalid, replace with latest
                latest_version = mgr.latest_version(package, lb, get_logged_in_username())
                version = latest_version

        # Return object
        return PackageComponent(manager=manager, package=package, version=version, latest_version=latest_version)
