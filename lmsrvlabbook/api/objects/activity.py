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
from graphene.types import datetime

from lmcommon.labbook import LabBook
from lmcommon.logging import LMLogger
from lmcommon.activity import ActivityStore, ActivityDetailRecord, ActivityDetailType, ActivityType

from lmsrvcore.auth.user import get_logged_in_username
from lmsrvcore.api import logged_query

logger = LMLogger.get_logger()

# Bring ActivityType enumeration into Graphene
ActivityRecordTypeEnum = graphene.Enum.from_enum(ActivityType)

# Bring ActivityDeatilType enumeration into Graphene
ActivityDetailTypeEnum = graphene.Enum.from_enum(ActivityDetailType)


class ActivityDetailObject(graphene.ObjectType):
    """Container for Activity Detail Records"""

    class Meta:
        interfaces = (graphene.relay.Node,)

    # Unique key for this activity detail record in the detail db
    key = graphene.String()

    # A list of data elements, encoded for the web, with the format [[MIME_TYPE, DATA],]
    data = graphene.List(graphene.List(graphene.String))

    # Type indicating the type of activity detail object
    type = graphene.Field(ActivityDetailTypeEnum)

    # Boolean indicating if this item should be "shown" or "hidden"
    show = graphene.Boolean()

    # A score indicating the importance, currently expected to range from 0-255
    importance = graphene.Int()

    # A list of tags for the entire record
    tags = graphene.List(graphene.String)

    @staticmethod
    def to_type_id(id_data):
        """Method to generate a single string that uniquely identifies this object

        Args:
            id_data(dict):

        Returns:
            str
        """
        return "{}&{}&{}".format(id_data["owner"], id_data["name"], id_data["key"])

    @staticmethod
    def parse_type_id(type_id):
        """Method to parse an ID for a given type into its identifiable variables returned as a dictionary of strings

        Args:
            type_id (str): type unique identifier

        Returns:
            dict
        """
        split = type_id.split("&")
        return {"owner": split[0], "name": split[1], "key": split[2]}

    @staticmethod
    @logged_query
    def create(id_data):
        """Method to create a graphene ActivityDetailObject object based on the node ID or owner+name+key

            {
                "type_id": <unique id for this object Type),
                "owner": <owner username (or org)>,
                "name": <name of the labbook>
                "key": <hash for the record>
            }

        Args:
            id_data(dict): A dictionary of variables that uniquely ID the instance. Can be a node ID or other vars

        Returns:
            NoteObject
        """
        try:
            if "type_id" in id_data:
                id_data.update(ActivityDetailObject.parse_type_id(id_data["type_id"]))
                del id_data["type_id"]

            if 'activity_store' not in id_data:
                lb = LabBook()
                lb.from_name(get_logged_in_username(), id_data["owner"], id_data["name"])

                # Create NoteStore instance
                id_data['activity_store'] = ActivityStore(lb)

            # Get detail record
            detail_record: ActivityDetailRecord = id_data['activity_store'].get_detail_record(id_data['key'])
            data = detail_record.jsonify_data()

            return ActivityDetailObject(id=ActivityDetailObject.to_type_id(id_data),
                                        key=detail_record.key,
                                        type=ActivityDetailTypeEnum.get(detail_record.type.value).value,
                                        show=detail_record.show,
                                        tags=detail_record.tags,
                                        importance=detail_record.importance,
                                        data=[(x, data[x]) for x in data],
                                        _id_data=id_data)
        except Exception as e:
            logger.error(e)
            raise

    @staticmethod
    def from_detail_record(detail_record, activity_store):
        """Method to create a graphene ActivityDetailObject object from a detail record already pulled from the note
         store

        Args:
            detail_record(ActivityDetailRecord): An ActivityDetailRecord instance
            activity_store(ActivityStore): An ActivityStore instance, used to resolve data if needed

        Returns:
            NoteObject
        """
        id_data = {"owner": activity_store.labbook.owner['username'],
                   "name": activity_store.labbook.name,
                   "key": detail_record.key,
                   'activity_store': activity_store
                   }

        return ActivityDetailObject(id=ActivityDetailObject.to_type_id(id_data),
                                    key=detail_record.key,
                                    type=ActivityDetailTypeEnum.get(detail_record.type.value).value,
                                    show=detail_record.show,
                                    tags=detail_record.tags,
                                    importance=detail_record.importance,
                                    _id_data=id_data)

    def resolve_data(self, args, context, info):
        """resolve the actual data for the detail object as a dict of MIME typed objects

        Args:
            args:
            context:
            info:

        Returns:

        """
        try:
            if 'activity_store' in self._id_data:
                store = self._id_data['activity_store']
            else:
                # Load labbook
                lb = LabBook()
                lb.from_name(get_logged_in_username(), self._id_data["owner"], self._id_data["name"])

                # Create ActivityStore instance
                store = ActivityStore(lb)

            detail_record: ActivityDetailRecord = store.get_detail_record(str(self.key))
            data = detail_record.jsonify_data()
            return [(x, data[x]) for x in data]
        except Exception as e:
            logger.error(e)
            raise


class ActivityRecordObject(graphene.ObjectType):
    """Container for Activity Records"""

    class Meta:
        interfaces = (graphene.relay.Node,)

    # Commit hash for this activity record
    commit = graphene.String()

    # Commit hash of the commit this references
    linked_commit = graphene.String()

    # Message summarizing the Activity
    message = graphene.String()

    # Storage for detail objects
    detail_objects = graphene.List(ActivityDetailObject)

    # Type indicating the type of activity
    type = graphene.Field(ActivityRecordTypeEnum)

    # Boolean indicating if this item should be "shown" or "hidden"
    show = graphene.Boolean()

    # A score indicating the importance, currently expected to range from 0-255
    importance = graphene.Int()

    # A list of tags for the entire record
    tags = graphene.List(graphene.String)

    # Datetime of the record creation
    timestamp = datetime.DateTime()

    @staticmethod
    def to_type_id(id_data):
        """Method to generate a single string that uniquely identifies this object

        Args:
            id_data(dict):

        Returns:
            str
        """
        return "{}&{}&{}".format(id_data["owner"], id_data["name"], id_data["commit"])

    @staticmethod
    def parse_type_id(type_id):
        """Method to parse an ID for a given type into its identifiable variables returned as a dictionary of strings

        Args:
            type_id (str): type unique identifier

        Returns:
            dict
        """
        split = type_id.split("&")
        return {"owner": split[0], "name": split[1], "commit": split[2]}

    @staticmethod
    @logged_query
    def create(id_data):
        """Method to create a graphene ActivityRecordObject object based on the node ID or owner+name+commit

            {
                "type_id": <unique id for this object Type),
                "owner": <owner username (or org)>,
                "name": <name of the labbook>
                "commit": <hash for the record>
            }

        Args:
            id_data(dict): A dictionary of variables that uniquely ID the instance. Can be a node ID or other vars

        Returns:
            NoteObject
        """
        try:
            if "type_id" in id_data:
                id_data.update(ActivityRecordObject.parse_type_id(id_data["type_id"]))
                del id_data["type_id"]

            lb = LabBook()
            lb.from_name(get_logged_in_username(), id_data["owner"], id_data["name"])

            # Create NoteStore instance
            activity_store = ActivityStore(lb)
            activity_record = activity_store.get_activity_record(id_data['commit'])
            detail_objects = [ActivityDetailObject.from_detail_record(r[3], activity_store) for r in activity_record.detail_objects]

            return ActivityRecordObject(id=ActivityRecordObject.to_type_id(id_data),
                                        commit=activity_record.commit,
                                        linked_commit=activity_record.linked_commit,
                                        message=activity_record.message,
                                        type=ActivityRecordTypeEnum.get(activity_record.type.value).value,
                                        show=activity_record.show,
                                        tags=activity_record.tags,
                                        timestamp=activity_record.timestamp,
                                        importance=activity_record.importance,
                                        detail_objects=detail_objects)
        except Exception as e:
            logger.error(e)
            raise

    @staticmethod
    def from_activity_record(activity_record, activity_store):
        """Method to create a graphene ActivityDetailObject object from an activity record already pulled from the note
         store

        Args:
            activity_record(ActivityRecord): An ActivityRecord instance
            activity_store(ActivityStore): An ActivityStore instance, used to resolve data if needed

        Returns:
            NoteObject
        """
        try:
            id_data = {"owner": activity_store.labbook.owner['username'],
                       "name": activity_store.labbook.name,
                       "commit": activity_record.commit
                       }

            detail_objects = [ActivityDetailObject.from_detail_record(r[3], activity_store) for r in
                              activity_record.detail_objects]

            return ActivityRecordObject(id=ActivityRecordObject.to_type_id(id_data),
                                        commit=activity_record.commit,
                                        linked_commit=activity_record.linked_commit,
                                        message=activity_record.message,
                                        type=ActivityRecordTypeEnum.get(activity_record.type.value).value,
                                        show=activity_record.show,
                                        tags=activity_record.tags,
                                        timestamp=activity_record.timestamp,
                                        importance=activity_record.importance,
                                        detail_objects=detail_objects)
        except Exception as e:
            logger.error(e)
            raise
