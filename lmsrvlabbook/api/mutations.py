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

from lmcommon.configuration import Configuration
from lmcommon.gitlib import get_git_interface
from lmcommon.labbook import LabBook
#from lmsrvcore.api import InputUser
#from lmsrvcore.api import get_logged_in_user
#from .objects import Labbook
#from .query import _get_graphene_labbook

from lmsrvlabbook.api.objects.labbook import CreateLabbook


class LabbookMutations(graphene.AbstractType):
    """Entry point for all graphql mutations"""
    create_labbook = CreateLabbook.Field()
    #create_branch = CreateBranch.Field()
    #checkout_branch = CheckoutBranch.Field()
