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
import shutil
import flask
from flask import Flask
import graphene
from graphene.test import Client
from mock import patch

from lmcommon.auth.identity import get_identity_manager
from lmcommon.configuration import Configuration
from lmcommon.workflows import BranchManager
from lmcommon.labbook import LabBook

from lmsrvcore.middleware import LabBookLoaderMiddleware, error_middleware
from lmsrvlabbook.tests.fixtures import ContextMock, fixture_working_dir
from lmsrvlabbook.api.query import LabbookQuery
from lmsrvlabbook.api.mutation import LabbookMutations

UT_USERNAME = "unittestbranchuser"
UT_LBNAME = "unittest-workflow-branch-1"


@pytest.fixture()
def mock_create_labbooks(fixture_working_dir):
    # Create a labbook in the temporary directory
    lb = LabBook(fixture_working_dir[0])
    lb.new(owner={"username": UT_USERNAME}, name=UT_LBNAME, description="Cats labbook 1")

    # Create a file in the dir
    with open(os.path.join(fixture_working_dir[1], 'unittest-examplefile'), 'w') as sf:
        sf.write("test data")
        sf.seek(0)
    lb.insert_file('code', sf.name, '')

    assert os.path.isfile(os.path.join(lb.root_dir, 'code', 'unittest-examplefile'))

    # Create test client
    schema = graphene.Schema(query=LabbookQuery, mutation=LabbookMutations)
    with patch.object(Configuration, 'find_default_config', lambda self: config_file):
        app = Flask("lmsrvlabbook")
        app.config["LABMGR_CONFIG"] = Configuration()
        app.config["LABMGR_ID_MGR"] = get_identity_manager(Configuration())
        with app.app_context():
            flask.g.user_obj = app.config["LABMGR_ID_MGR"].get_user_profile()
            client = Client(schema, middleware=[LabBookLoaderMiddleware(), error_middleware],
                            context_value=ContextMock())
            yield lb, client, schema
    shutil.rmtree(fixture_working_dir, ignore_errors=True)


class TestWorkflowsBranching(object):
    def test_active_branch_name(self, mock_create_labbooks):
        lb, client = mock_create_labbooks[0], mock_create_labbooks[1]
        bm = BranchManager(lb, username=UT_USERNAME)

        q = f"""
        {{
            labbook(name: "{UT_LBNAME}", owner: "{UT_USERNAME}") {{
                activeBranchName
            }}
        }}
        """
        r = client.execute(q)
        assert 'errors' not in r
        assert r['data']['labbook']['activeBranchName'] == bm.active_branch

    def test_available_branches(self, mock_create_labbooks):
        lb, client = mock_create_labbooks[0], mock_create_labbooks[1]
        bm = BranchManager(lb, username=UT_USERNAME)

        q = f"""
        {{
            labbook(name: "{UT_LBNAME}", owner: "{UT_USERNAME}") {{
                availableBranchNames
            }}
        }}
        """
        r = client.execute(q)
        assert 'errors' not in r
        assert r['data']['labbook']['activeBranchName'] == bm.active_branch

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
