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
import pytest
import tempfile
import os
from datetime import datetime
from snapshottest import snapshot
from lmsrvlabbook.tests.fixtures import fixture_working_dir, fixture_working_dir_populated_scoped, fixture_test_file

from graphene.test import Client
import graphene
from mock import patch
import pprint

from lmcommon.labbook import LabBook
from lmcommon.fixtures import remote_labbook_repo
from lmcommon.configuration import Configuration

from ..api import LabbookMutations, LabbookQuery


# Create ObjectType clases, since the LabbookQueries and LabbookMutations are abstract (allowing multiple inheritance)
class Query(LabbookQuery, graphene.ObjectType):
    pass


class Mutation(LabbookMutations, graphene.ObjectType):
    pass


class TestLabManagerQueries(object):

    def test_get_build_info(self, fixture_working_dir):
        """Test listing labbooks"""

        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir[0]):
            query = """
            {
                buildInfo
            }
            """
            client = Client(fixture_working_dir[2])
            r = client.execute(query)
            pprint.pprint(r)
            assert 'errors' not in r
            assert '-' in r['data']['buildInfo']
