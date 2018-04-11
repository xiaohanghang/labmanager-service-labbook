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

from lmcommon.logging import LMLogger
from lmcommon.labbook import LabBook
from lmcommon.workflows import BranchManager
from lmcommon.activity import ActivityStore, ActivityDetailRecord, ActivityDetailType, ActivityRecord, ActivityType

from lmsrvcore.auth.user import get_logged_in_username, get_logged_in_author
from lmsrvlabbook.api.objects.labbook import Labbook

logger = LMLogger.get_logger()


class CreateExperimentalBranch(graphene.relay.ClientIDMutation):
    """Mutation to create a local experimental (or Rollback) branch. """

    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        branch_name = graphene.String(required=True)
        revision = graphene.String()
        description = graphene.String()

    labbook = graphene.Field(Labbook)

    @classmethod
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, branch_name, revision=None,
                               description=None, client_mutation_id=None):
        username = get_logged_in_username()
        lb = LabBook(author=get_logged_in_author())
        lb.from_name(username, owner, labbook_name)
        bm = BranchManager(labbook=lb, username=username)
        full_branch_title = bm.create_branch(title=branch_name, revision=revision)
        logger.info(f"In {str(lb)} created new experimental feature branch {full_branch_title}")

        # TODO: Refactor description implementation into BranchManager.create_branch()
        if description:
            # Update the description on branch creation
            lb.description = description

            with lb.lock_labbook():
                lb.git.add(os.path.join(lb.root_dir, '.gigantum/labbook.yaml'))
                commit = lb.git.commit('Updating description')

                # Create detail record
                adr = ActivityDetailRecord(ActivityDetailType.LABBOOK, show=False)
                adr.add_value('text/plain', description)

                # Create activity record
                ar = ActivityRecord(ActivityType.LABBOOK,
                                    message="Updated description of LabBook",
                                    linked_commit=commit.hexsha,
                                    tags=["labbook"],
                                    show=False)
                ar.add_detail_object(adr)

                # Store
                ars = ActivityStore(lb)
                ars.create_activity_record(ar)
                logger.info(f"In {str(lb)} update description")

        return CreateExperimentalBranch(labbook=Labbook(id="{}&{}".format(owner, labbook_name),
                                                        name=labbook_name, owner=owner))


class DeleteExperimentalBranch(graphene.relay.ClientIDMutation):
    """Delete a feature/rollback branch. Fails for any other attempt."""

    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        branch_name = graphene.String(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, branch_name, client_mutation_id=None):
        username = get_logged_in_username()
        lb = LabBook(author=get_logged_in_author())
        lb.from_name(username, owner, labbook_name)
        bm = BranchManager(labbook=lb, username=username)
        bm.remove_branch(target_branch=branch_name)
        logger.info(f'Removed experimental branch {branch_name} from {str(lb)}')
        return DeleteExperimentalBranch(success=True)


class WorkonBranch(graphene.relay.ClientIDMutation):
    """Work on another branch (perform a git checkout)."""

    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        branch_name = graphene.String(required=True)
        revision = graphene.String()

    labbook = graphene.Field(Labbook)

    @classmethod
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, branch_name, client_mutation_id=None):
        username = get_logged_in_username()
        lb = LabBook(author=get_logged_in_author())
        lb.from_name(username, owner, labbook_name)
        bm = BranchManager(labbook=lb, username=username)
        bm.workon_branch(branch_name=branch_name)
        return WorkonBranch(labbook=Labbook(id="{}&{}".format(owner, labbook_name),
                                            name=labbook_name, owner=owner))


class MergeFromBranch(graphene.relay.ClientIDMutation):
    """Merge from another branch into the current active branch. Force if necessary. """

    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        other_branch_name = graphene.String(required=True)
        force = graphene.Boolean()

    labbook = graphene.Field(Labbook)

    @classmethod
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, other_branch_name, force=False,
                               client_mutation_id=None):
        username = get_logged_in_username()
        lb = LabBook(author=get_logged_in_author())
        lb.from_name(username, owner, labbook_name)
        bm = BranchManager(labbook=lb, username=username)
        bm.merge_from(other_branch=other_branch_name, force=force)

        return MergeFromBranch(labbook=Labbook(id="{}&{}".format(owner, labbook_name),
                                               name=labbook_name, owner=owner))
