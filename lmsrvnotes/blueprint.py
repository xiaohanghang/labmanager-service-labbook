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
from flask import Blueprint
from flask_graphql import GraphQLView
import graphene

from .api import NoteQueries, NoteMutations

from lmcommon.configuration import Configuration


# Create ObjectType clases, since the NoteQueries and NoteMutations are abstract (allowing multiple inheritance)
class Query(NoteQueries, graphene.ObjectType):
    pass


class Mutation(NoteMutations, graphene.ObjectType):
    pass


# Load config data for the LabManager instance
config = Configuration()

# Create Blueprint
notes_service = Blueprint('notes_service', __name__)

# Add route
notes_service.add_url_rule('/labbook/',
                           view_func=GraphQLView.as_view('graphql',
                                                         schema=graphene.Schema(query=Query,
                                                                                mutation=Mutation),
                                                         graphiql=config.config["flask"]["DEBUG"]))
