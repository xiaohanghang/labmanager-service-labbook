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
from graphene import resolve_only_args
import json
import re

from lmcommon.api.util import get_logged_in_user

from .objects import Notes, NoteSummary, Note, NoteObject, LogLevel
from lmcommon.labbook import LabBook
from lmcommon.notes import NoteStore


class NoteQueries(graphene.AbstractType):
    """Queries that get lists of notes from git repositories"""
    # List note
    note_summaries = graphene.Field(Notes, labbook_name=graphene.String())

    # Get an individual note
    note = graphene.Field(Note, labbook_name=graphene.String(), commit=graphene.String())

    @resolve_only_args
    def resolve_note_summaries(self, labbook_name):
        # TODO: Lookup name based on logged in user when available
        username = get_logged_in_user()

        # Load LabBook instance
        lb = LabBook()
        lb.from_name(username, labbook_name)

        # retrieve a list of notes from the commit log.
        lblog = lb.log(max_count=100)

        # empty list of notes
        notes = []

        # filter log on Notes
        regex = r"gtmNOTE_: ([\w\s\S]+)\ngtmjson_metadata_: (.*)"
        for entry in lblog:
            m = re.match(regex, entry['message'])
            if m:
                message = m.group(1)
                note_metadata = json.loads(m.group(2))

                # add a NoteSummary object to output
                notes.append(NoteSummary(labbook_name=labbook_name,
                                         level=note_metadata['level'],
                                         commit=entry['commit'],
                                         author=entry['author'],
                                         timestamp=entry['committed_on'],
                                         linked_commit=note_metadata['linked_commit'],
                                         tags=note_metadata['tags'],
                                         message=message))
              
        # retrieve a list of notes from the commit log.
        return Notes(labbook_name=labbook_name, entries=notes)

    @resolve_only_args
    def resolve_note(self, labbook_name, commit):
        # TODO: Lookup name based on logged in user when available
        username = get_logged_in_user()

        # Load LabBook instance
        lb = LabBook()
        lb.from_name(username, labbook_name)

        # Create NoteStore instance
        ns = NoteStore(lb)

        # get the record for the individual commit
        entry = lb.log_entry(commit=commit)

        # filter log on Notes
        regex = r"gtmNOTE_: ([\w\s\S]+)\ngtmjson_metadata_: (.*)"

        m = re.match(regex, entry['message'])
        if m:
            # summary data from git log
            message = m.group(1)
            note_metadata = json.loads(m.group(2))

            # get the detail from notes storage.
            note_detail = ns.get_entry(note_metadata["linked_commit"])

            # deep copy of the input noteobjects -- list comprehension doesn't work
            note_objects = []
            for i in json.loads(note_detail['objects']):
                nobj = NoteObject(key=i['key'], object_type=i['object_type'], value=i['value'])
                note_objects.append(nobj)
        else:
            raise ValueError("Commit {} not found".format(commit))

        return Note(labbook_name=labbook_name,
                    level=note_metadata['level'],
                    commit=entry['commit'],
                    timestamp=entry['committed_on'],
                    linked_commit=note_metadata['linked_commit'],
                    author=entry['author'],
                    tags=note_metadata['tags'],
                    message=message,
                    free_text=note_detail['free_text'],
                    objects=note_objects)
