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
import os
import pytest

from snapshottest import snapshot
from lmsrvlabbook.tests.fixtures import fixture_working_dir
from lmcommon.configuration import Configuration
from lmcommon.labbook import LabBook

from graphene.test import Client
import graphene
from mock import patch


@pytest.fixture()
def mock_create_labbooks(fixture_working_dir):
    # Create a labbook in the temporary directory
    lb = LabBook(fixture_working_dir[0])
    lb.new(owner={"username": "default"}, name="labbook1", description="Cats labbook 1")

    # Create a file in the dir
    with open(os.path.join(fixture_working_dir[1], 'sillyfile'), 'w') as sf:
        sf.write("1234567")
        sf.seek(0)
    lb.insert_file('code', sf.name, '')

    assert os.path.isfile(os.path.join(lb.root_dir, 'code', 'sillyfile'))
    # name of the config file, temporary working directory, the schema
    yield fixture_working_dir


class TestWorkflowsBranching(object):
    def test_active_branch_name(self):
        pass

    def test_available_branches(self):
        pass

    def test_query_mergeable_branches_from_main(self):
        pass

    def test_query_mergeable_branches_from_feature_branch(self):
        pass

    def test_create_feature_branch_bad_name_fail(self):
        pass

    def test_create_feature_branch_from_feature_branch_fail(self):
        pass

    def test_create_feature_branch_success(self):
        pass

    def test_delete_feature_branch_fail(self):
        pass

    def test_delete_feature_branch_success(self):
        pass

    def test_workon_feature_branch_bad_name_fail(self):
        pass

    def test_workon_feature_branch_success(self):
        pass

    def test_merge_from_simple_success(self):
        pass

    def test_conflicted_merge_from_no_force_fail(self):
        pass

    def test_conflicted_merge_from_force_success(self):
        pass
