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
from datetime import datetime
import json
import re

from .objects import Notes, NoteSummary, Note, LogLevel
from lmcommon.labbook import LabBook


class NotesQueries(graphene.ObjectType):
    """Queries that get lists of notes from git repositories"""

    notes = graphene.Field(Notes, lbname=graphene.String())

    @resolve_only_args
    def resolve_notes(self, lbname):

        lb = LabBook()

        # TODO: Lookup lbname based on logged in user
        lb.from_name("default", lbname)

        # retrieve a list of notes from the commit log.
        lblog = lb.log(max_count=100)

        # empty list of notes
        notes = []

        # filter log on Notes
        regex=r"gtmNOTE_: ([\w\s\S]+)\ngtmjson_metadata_: (.*)"
        for entry in lblog:

            m = re.match(regex, entry['message'])
            if m:
            
                message = m.group(1)
                notemd = json.loads(m.group(2))

                # add a NoteSummary object to output
                notes.append (NoteSummary (lbname=lbname, level=LogLevel(notemd['level']), commit=entry['commit'], timestamp=entry['committed_on'], linkedcommit=notemd['linkedcommit'], tags=notemd['tags'], message=message )) 
              
        
        # retrieve a list of notes from the commit log.

        # RBTODO get the list of notes from the labbook
        return Notes(lbname=lbname, entries=notes) 


class NoteQueries(graphene.ObjectType):
    """Queries that interact with a single note"""

    note = graphene.Field(Note, lbname=graphene.String(), commit=graphene.ID())

    @resolve_only_args
    def resolve_note(self, lbname, commit):

        lb = LabBook()

        # TODO: Lookup lbname based on logged in user
        lb.from_name("default", lbname)

        # get the record for the individual commit
        entry = lb.log_entry(commit=commit)

        # filter log on Notes
        regex=r"gtmNOTE_: ([\w\s\S]+)\ngtmjson_metadata_: (.*)"

        m = re.match(regex, entry['message'])
        if m:
            message = m.group(1)
            notemd = json.loads(m.group(2))

        return Note (lbname=lbname, level=LogLevel(notemd['level']), commit=entry['commit'], timestamp=entry['committed_on'], linkedcommit=notemd['linkedcommit'], tags=notemd['tags'], message=message, freetext="freetext7", kvobjects=json.dumps([["7","seven"],["8","Eight"]])) 
  

