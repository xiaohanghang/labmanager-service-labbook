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

from .objects import Notes, NoteSummary, Note
from lmcommon.labbook import LabBook


class NotesQueries(graphene.ObjectType):
    """Queries that get lists of notes from git repositories"""

    notes = graphene.Field(Notes, lbname=graphene.String())

    @resolve_only_args
    def resolve_notes(self, lbname):
        lb = LabBook()

        # TODO: Lookup lbname based on logged in user
        lb.from_name("default", lbname)

        # RBTODO get the list of notes from the labbook
        note1 = NoteSummary ( lbname=lbname, id=1, loglevel="User1", tags=["tag1","tag2"], timestamp=datetime.now(), message="commit1" )
        note2 = NoteSummary ( lbname=lbname, id=2, loglevel="User2", tags=["tag2.1","tag2.2"], timestamp=datetime.now(), message="commit1" )

        commitlog = { note1, note2  }
       
        return Notes(lbname=lbname, entries=commitlog) 


class NoteQueries(graphene.ObjectType):
    """Queries that interact with a single note"""

    note = graphene.Field(Note, lbname=graphene.String(), id=graphene.ID())

    @resolve_only_args
    def resolve_note(self, lbname, id):

#        lb = LabBook()
#    
#        lbcommit = lb.commit_by_id(id)
#
#        return Note(NoteSummary,Not)

        return Note ( lbname=lbname, id=id, loglevel="User3", tags=["tag3.1","tag3.2"], timestamp=datetime.now(), message="commit3" , freetext="freetext7", kvobjects=json.dumps([["7","seven"],["8","Eight"]])) 
  

