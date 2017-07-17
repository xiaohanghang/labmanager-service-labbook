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
from lmsrvcore.api import get_logged_in_user
from .objects import Note, LogLevel, NoteObject, NoteObjectInput


class CreateNote(graphene.Mutation):
    """Mutation to create a new note entry"""

    class Input:
        labbook_name = graphene.String(required=True)
        level = LogLevel(required=True)
        message = graphene.String()
        linked_commit = graphene.String()
        tags = graphene.List(graphene.String)
        free_text = graphene.String()
        objects = graphene.List(NoteObjectInput)

    # Return the Note
    note = graphene.Field(lambda: Note)

    @staticmethod
    def mutate(root, args, context, info):
        # TODO: Lookup name based on logged in user when available
        username = get_logged_in_user()

        # Load LabBook instance
        lb = LabBook()
        lb.from_name(username, args.get('labbook_name'))

        note_metadata = {'level': args.get('level'),
                         'linked_commit': args.get('linked_commit'),
                         'tags': args.get('tags')}

        # format note metadata into message
        message = "gtmNOTE_: {}\ngtmjson_metadata_: {}".format(args.get('message'), json.dumps(note_metadata))

        try:
            # Instantiate the notes detailed store and save detail to local db
            ns = NoteStore(lb)
            nsdict = {'free_text': args.get('free_text'), 'objects': json.dumps(args.get('objects'))}

            # Create record using the linked_commit hash as the reference
            ns.put_entry(str(args.get('linked_commit')), nsdict)
        except Exception as err:
            raise IOError("Failed to store note detail: {}".format(err))

        # Add everything in the LabBook notes/log directory in case it is new or a new log file has been created
        lb.git.add_all(os.path.expanduser(os.path.join(".gigantum", "notes", "log")))

        # Commit the changes as you've updated the notes DB
        notecommit = lb.commit(message)

        # deep copy of the input noteobjects -- list comprehension doesn't work
        nobjects = []
        for i in args.get('objects'):
            nobj = NoteObject(key=i['key'], object_type=i['object_type'], value=i['value'])
            nobjects.append(nobj)

        note = Note(labbook_name=args.get('labbook_name'),
                    commit=notecommit,
                    linked_commit=args.get("linked_commit"),
                    level=args.get('level'),
                    tags=args.get('tags'),
                    timestamp=datetime.utcnow(),
                    message=args.get('message'),
                    free_text=args.get('free_text'),
                    objects=nobjects)

        return CreateNote(note=note)


class NoteMutations(graphene.AbstractType):
    """Entry point for all Note service mutations"""
    create_note = CreateNote.Field()

