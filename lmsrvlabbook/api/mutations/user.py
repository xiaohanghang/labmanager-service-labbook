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
import flask
import graphene

from lmsrvcore.api.objects.user import UserIdentity

from lmcommon.configuration import Configuration
from lmcommon.logging import LMLogger

logger = LMLogger.get_logger()


class RemoveUserIdentity(graphene.relay.ClientIDMutation):
    """Mutation to remove a locally stored user identity (no-op if not running in local mode)"""

    # Return the Note
    user_identity_edge = graphene.Field(lambda: UserIdentity)

    @classmethod
    def mutate_and_get_payload(cls, root, input, client_mutation_id=None):
        # Check if there is a local user identity, remove if needed
        identity_file = os.path.join(Configuration().config['git']['working_directory'],
                                     '.labmanager', 'identity', 'user.json')
        if os.path.exists(identity_file):
            os.remove(identity_file)
        else:
            # Does not exist
            logger.warning("Attempted to remove user identity, but no identity is stored locally.")

        # Wipe current user from session
        flask.g.user_obj = None

        return RemoveUserIdentity(user_identity_edge=UserIdentity())
