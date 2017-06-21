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
import uuid

import graphene

import json
from datetime import datetime


from .objects import Note

from lmcommon.labbook import LabBook

#class NoteKVFields(graphene.ObjectType):
#    """Container for arbitrary key/value.  
#        * keys are strings.
#        * values are uninterpreted blobs encoded as strings?
#    """
#    key = graphene.String()
#    value = graphene.String()


class CreateNote(graphene.Mutation):
    """Class for Mutator.  Don't use camel case in suffix, i.e. Labbook not LabBook """

    # RBTODO wire up optional input.
#    class input:
#      lbname = graphene.String()
#      message = graphene.String()
#      loglevel = graphene.String()

    # Return the Note
    note = graphene.Field(lambda: Note)

    @staticmethod
    def mutate(root, args, context, info):

 # Create a new empty LabBook
        # lookup the labbook by name
        # validate that the id points to a good commit record
        # add the commit mesage to the git log
#        lbnote = lb.new_note (loglevel=args.get('loglevel'), commit_id = args.get('commit_id'),  
#                        timestamp=datetime.now(), message=args.get('message'))
        # add the details to the notes log.

        # RBTODO separate commit id and ID
        note = Note( lbname="Some Name", id=7, loglevel="warn", tags=["tag11.1","tags11.2"], timestamp=datetime.now(), message="message11", freetext="freetext11", kvobjects=json.dumps([["11","ounces"],["8","hours"]]))
#        note = Note( name=args.get('lbname'), id=7, loglevel=args.get('loglevel'), 
#                        tags=["tag11.1","tags11.2"], timestamp=datetime.now(), message=args.get('message'),
#                        freetext="freetext11", kvobjects=json.dumps([["11","ounces"],["8","hours"]]))

        return CreateNote(note=note)


class NoteMutations(graphene.ObjectType):
    """Entry point for all graphql mutations"""
    create_note = CreateNote.Field()

