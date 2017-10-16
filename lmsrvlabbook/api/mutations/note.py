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
import json
import os
from datetime import datetime

import graphene

from lmcommon.labbook import LabBook
from lmcommon.notes import NoteStore
from lmsrvcore.auth.user import get_logged_in_user

from lmsrvlabbook.api.objects.note import Note, NoteLogLevelEnum
from lmsrvlabbook.api.objects.noteobject import NoteObjectInput


class CreateNote(graphene.relay.ClientIDMutation):
    """Mutation to create a new note entry"""

    class Input:
        labbook_name = graphene.String(required=True)
        owner = graphene.String()
        level = graphene.Field(NoteLogLevelEnum, required=True)
        message = graphene.String(required=True)
        linked_commit = graphene.String(required=True)
        tags = graphene.List(graphene.String)
        free_text = graphene.String()
        objects = graphene.List(NoteObjectInput)

    # Return the Note
    note = graphene.Field(lambda: Note)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        # TODO: Lookup name based on logged in user when available
        username = get_logged_in_user()

        if not input.get("owner"):
            owner = username
        else:
            owner = input.get("owner")

        # Load LabBook instance
        lb = LabBook()
        lb.from_name(username, owner, input.get('labbook_name'))

        # Create NoteStore instance
        note_db = NoteStore(lb)

        note_data = {'linked_commit': input.get('linked_commit'),
                     'message': input.get('message'),
                     'level': input.get('level'),
                     'tags': input.get('tags'),
                     'free_text': input.get('free_text'),
                     'objects': input.get('objects')}

        # Create a note record
        note_commit = note_db.create_note(note_data)

        # Read data back to ensure it was written
        note = note_db.get_note(note_commit.hexsha)

        note_obj = Note(id=Note.to_type_id({'name': input.get('labbook_name'),
                                            'owner': owner,
                                            'commit': note_commit}),
                        commit=note['note_commit'],
                        linked_commit=note["linked_commit"],
                        note_detail_key=note["note_detail_key"],
                        level=note['level'].value,
                        tags=note['tags'],
                        timestamp=note['timestamp'],
                        message=note['message'],
                        author=note['author']['email'],
                        free_text=note['free_text'],
                        objects=note['objects'])

        return CreateNote(note=note_obj)


class CreateUserNote(graphene.relay.ClientIDMutation):
    """Mutation to create a new user note entry in the activity feed of lab book

    The log level is set to USER_NOTE automatically and the `linked_commit` is an empty string

    """

    class Input:
        labbook_name = graphene.String(required=True)
        owner = graphene.String()
        message = graphene.String(required=True)
        free_text = graphene.String()
        tags = graphene.List(graphene.String)
        objects = graphene.List(NoteObjectInput)

    # Return the Note
    note = graphene.Field(lambda: Note)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        # TODO: Lookup name based on logged in user when available
        username = get_logged_in_user()

        if not input.get("owner"):
            owner = username
        else:
            owner = input.get("owner")

        # Load LabBook instance
        lb = LabBook()
        lb.from_name(username, owner, input.get('labbook_name'))

        # Create NoteStore instance
        note_db = NoteStore(lb)

        note_data = {'note_detail_key': None,
                     'linked_commit': None,
                     'message': input.get('message'),
                     'level': NoteLogLevelEnum.USER_NOTE,
                     'tags': input.get('tags'),
                     'free_text': input.get('free_text'),
                     'objects': input.get('objects')}

        # Create a note record
        note_commit = note_db.create_note(note_data)

        # Read data back to ensure it was written
        note = note_db.get_note(note_commit.hexsha)

        note_obj = Note(id=Note.to_type_id({'name': input.get('labbook_name'),
                                            'owner': owner,
                                            'commit': note_commit}),
                        commit=note['note_commit'],
                        linked_commit=note['linked_commit'],
                        note_detail_key=note['note_detail_key'],
                        level=note['level'].value,
                        tags=note['tags'],
                        timestamp=note['timestamp'],
                        message=note['message'],
                        author=note['author']['email'],
                        free_text=note['free_text'],
                        objects=note['objects'])

        return CreateUserNote(note=note_obj)
