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
import time

import graphene


from lmcommon.labbook import LabBook
from lmcommon.container.container import ContainerOperations
from lmcommon.logging import LMLogger
from lmcommon.activity.services import start_labbook_monitor

from lmsrvcore.auth.user import get_logged_in_username, get_logged_in_author

logger = LMLogger.get_logger()


class StartDevTool(graphene.relay.ClientIDMutation):
    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        dev_tool = graphene.String(required=True)
        container_override_id = graphene.String(required=False)

    # Return the Environment instance
    path = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, dev_tool,
                               container_override_id=None, client_mutation_id=None):
        username = get_logged_in_username()
        lb = LabBook(author=get_logged_in_author())
        lb.from_name(username, owner, labbook_name)
        lb, tool_url = ContainerOperations.start_dev_tool(lb, dev_tool_name=dev_tool, username=username,
                                                          tag=container_override_id)

        # Start monitoring lab book environment for activity
        start_labbook_monitor(lb, username, dev_tool, author=get_logged_in_author())
        
        return StartDevTool(path=tool_url)
