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
from .objects import Notes

from lmcommon.labbook import LabBook

class NoteKVFields(graphene.ObjectType):
    """Container for arbitrary key/value.  
        * keys are strings.
        * values are uninterpreted blobs encoded as strings?
    """
    key = graphene.String()
    value = graphene.String()


class CreateNote(graphene.Mutation):
    """Class for Mutator.  Don't use camel case in suffix, i.e. Labbook not LabBook """

    class input:
      name = graphene.String()
      commit_id = graphene.ID()
      loglevel = graphene.String()
      message = graphene.ID()
#
#  RBTODO these fields will go into notes log.
#      freetext = graphene.String()
#      kvobjects = graphene.list(NoteKVFields)

    @staticmethod
    def mutate(root, args, context, info):
        lb = LabBook()

        # TODO: Lookup name based on logged in user
        lb.from_name("default", name)

        # add the commit mesage to the git log
        lbnote = lb.new_note (loglevel=args.get('loglevel'), commit_id = args.get('commit_id'),  
                        timestamp=datetime.now(), message=args.get('message'))

        #RBTODO finish
        #RBTODO finish
        note = CreateNote ( lb

      return 


class NotesMutations(graphene.ObjectType):
    """Entry point for all graphql mutations"""

