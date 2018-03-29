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
from lmcommon.labbook import LabBook
from lmcommon.workflows import BranchManager

from lmsrvcore.auth.user import get_logged_in_username, get_logged_in_author

logger = LMLogger.get_logger()


class CreateExperimentalBranch(graphene.relay.ClientIDMutation):
    """Mutation to create a local experimental (or Rollback) branch. """

    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        branch_name = graphene.String(required=True)
        revision = graphene.String()

    new_branch_name = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, branch_name, revision=None, client_mutation_id=None):
        username = get_logged_in_username()
        lb = LabBook(author=get_logged_in_author())
        lb.from_name(username, owner, labbook_name)
        bm = BranchManager(labbook=lb, username=username)
        full_branch_title = bm.create_branch(title=branch_name, revision=revision)
        logger.info(f"In {str(lb)} created new experimental feature branch {full_branch_title}")
        return CreateExperimentalBranch(new_branch_name=full_branch_title)


class DeleteExperimentalBranch(graphene.relay.ClientIDMutation):
    """Mutation to create a local experimental (or Rollback) branch. """

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
    """Mutation to create a local experimental (or Rollback) branch. """

    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        branch_name = graphene.String(required=True)
        revision = graphene.String()

    current_branch_name = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, branch_name, client_mutation_id=None):
        username = get_logged_in_username()
        lb = LabBook(author=get_logged_in_author())
        lb.from_name(username, owner, labbook_name)
        bm = BranchManager(labbook=lb, username=username)
        bm.workon_branch(target_branch=branch_name)
        return WorkonBranch(current_branch_name=bm.active_branch)


class MergeFromBranch(graphene.relay.ClientIDMutation):
    """Mutation to create a local experimental (or Rollback) branch. """

    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        other_branch_name = graphene.String(required=True)
        force = graphene.Boolean()

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, other_branch_name, force=False, client_mutation_id=None):
        username = get_logged_in_username()
        lb = LabBook(author=get_logged_in_author())
        lb.from_name(username, owner, labbook_name)
        bm = BranchManager(labbook=lb, username=username)
        bm.merge_from(other_branch=other_branch_name, force=force)
        return MergeFromBranch(success=True)
