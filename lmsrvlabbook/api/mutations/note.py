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

from lmcommon.labbook import LabBook
from lmcommon.logging import LMLogger

from lmcommon.activity import ActivityStore, ActivityDetailRecord, ActivityDetailType, ActivityRecord, ActivityType
from lmsrvcore.auth.user import get_logged_in_username

from lmsrvcore.api import logged_mutation
from lmsrvlabbook.api.objects.activity import ActivityRecordObject
from lmsrvlabbook.api.connections.activity import ActivityConnection

logger = LMLogger.get_logger()


class CreateUserNote(graphene.relay.ClientIDMutation):
    """Mutation to create a new user note entry in the activity feed of lab book

    The `linked_commit` is an empty string since there is no linked commit

    """

    class Input:
        owner = graphene.String(required=False)
        labbook_name = graphene.String(required=True)
        title = graphene.String(required=True)
        body = graphene.String(required=False)
        tags = graphene.List(graphene.String, required=False)

    # Return the new Activity Record
    new_activity_record_edge = graphene.Field(lambda: ActivityConnection.Edge)

    @classmethod
    @logged_mutation
    def mutate_and_get_payload(cls, input, context, info):
        username = get_logged_in_username()

        if not input.get("owner"):
            owner = username
        else:
            owner = input.get("owner")

        # Load LabBook instance
        lb = LabBook()
        lb.from_name(username, owner, input.get('labbook_name'))

        # Create a Activity Store instance
        store = ActivityStore(lb)

        # Create detail record
        adr = ActivityDetailRecord(ActivityDetailType.NOTE,
                                   show=True,
                                   importance=255)
        if input.get("body"):
            adr.add_value('text/markdown', input.get("body"))

        # Create activity record
        ar = ActivityRecord(ActivityType.NOTE,
                            message=input.get("title"),
                            linked_commit="xxx",
                            importance=255,
                            tags=input.get("tags"))
        ar.add_detail_object(adr)
        ar = store.create_activity_record(ar)

        return CreateUserNote(new_activity_record_edge=ActivityConnection.Edge(node=ActivityRecordObject.from_activity_record(ar, store),
                                                                               cursor=ar.commit))
