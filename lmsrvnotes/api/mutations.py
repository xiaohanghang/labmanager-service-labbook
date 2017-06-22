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

from .objects import Note, LogLevel, NoteObject, NoteObjectIn

from lmcommon.labbook import LabBook
from lmcommon.gitlib import GitAuthor
from lmcommon.notes import NoteStore


class CreateNote(graphene.Mutation):
    """Class for Mutator.  Don't use camel case in suffix, i.e. Labbook not LabBook """

    class Input:
        lbname = graphene.String(required=True)
        level = LogLevel(required=True)
        message = graphene.String()
        linkedcommit = graphene.String()
        tags = graphene.List(graphene.String)
        freetext = graphene.String()
        objects = graphene.List(NoteObjectIn)

    # Return the Note
    note = graphene.Field(lambda: Note)

    @staticmethod
    def mutate(root, args, context, info):

        # lookup the labbook by name
        lb = LabBook()
        lb.from_name("default", args.get('lbname'))

        notesmd = { 'level': args.get('level'),
                    'linkedcommit': args.get('linkedcommit'),
                    'tags': args.get('tags') }

        # format note metadata into message
        message = "gtmNOTE_: {}\ngtmjson_metadata_: {}".format(args.get('message'),json.dumps(notesmd))
        notecommit = lb.commit(message)

        try:
            # instantiate the notes detailed store
            ns = NoteStore(lb)
            nsdict = { 'freetext': args.get('freetext'), 'objects': json.dumps(args.get('objects')) }
            ns.putEntry(str(notecommit), nsdict)
        except:
            raise #TODO what compensating action?

        # deep copy of the input noteobjects -- list comprehension doesn't work
        nobjects= []
        for i in args.get('objects'):
            nobj = NoteObject(key=i['key'], objecttype=i['objecttype'], value=i['value'])
            nobjects.append(nobj)

        note = Note( lbname=args.get('lbname'), commit=notecommit, linkedcommit=args.get("linkedcommit"), level=args.get('level'), tags=args.get('tags'), timestamp=datetime.now(), message=args.get('message'), freetext=args.get('freetext'), objects=nobjects)

        return CreateNote(note=note)


class NoteMutations(graphene.ObjectType):
    """Entry point for all graphql mutations"""
    create_note = CreateNote.Field()

