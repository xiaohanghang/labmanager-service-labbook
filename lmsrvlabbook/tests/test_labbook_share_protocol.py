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
import io
import math
import os
import responses
import tempfile
import datetime
import pprint
from zipfile import ZipFile
from pkg_resources import resource_filename
import getpass

import git

from snapshottest import snapshot
from lmsrvlabbook.tests.fixtures import fixture_working_dir_env_repo_scoped, fixture_working_dir

import pytest
from graphene.test import Client
from mock import patch
from werkzeug.test import EnvironBuilder
from werkzeug.wrappers import Request
from werkzeug.datastructures import FileStorage

from lmcommon.configuration import Configuration
from lmcommon.dispatcher.jobs import export_labbook_as_zip
from lmcommon.fixtures import (remote_labbook_repo, remote_bare_repo, mock_labbook,
                               mock_config_file, _MOCK_create_remote_repo)
from lmcommon.labbook import LabBook


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


class TestLabbookShareProtocol(object):
    @patch('lmcommon.labbook.LabBook._create_remote_repo', new=_MOCK_create_remote_repo)
    def test_publish_basic(self, fixture_working_dir, remote_bare_repo, mock_create_labbooks):

        # Mock the request context so a fake authorization header is present
        builder = EnvironBuilder(path='/labbook', method='POST', headers={'Authorization': 'Bearer AJDFHASD'})
        env = builder.get_environ()
        req = Request(environ=env)

        test_user_lb = LabBook(mock_create_labbooks[0])
        test_user_lb.from_name('default', 'default', 'labbook1')

        publish_query = f"""
        mutation c {{
            publishLabbook(input: {{
                labbookName: "labbook1",
                owner: "default"
            }}) {{
                success
            }}
        }}
        """

        r = fixture_working_dir[2].execute(publish_query, context_value=req)
        assert 'errors' not in r
        assert r['data']['publishLabbook']['success'] is True

    @responses.activate
    @patch('lmcommon.labbook.LabBook._create_remote_repo', new=_MOCK_create_remote_repo)
    def test_sync_1(self, fixture_working_dir, remote_bare_repo, mock_create_labbooks, mock_labbook, mock_config_file):

        # Setup responses mock for this test
        responses.add(responses.GET, 'https://usersrv.gigantum.io/key',
                      json={'key': 'afaketoken'}, status=200)

        test_user_lb = LabBook(mock_create_labbooks[0])
        test_user_lb.from_name('default', 'default', 'labbook1')
        test_user_lb.publish('default')

        # Mock the request context so a fake authorization header is present
        builder = EnvironBuilder(path='/labbook', method='POST', headers={'Authorization': 'Bearer AJDFHASD'})
        env = builder.get_environ()
        req = Request(environ=env)

        remote_url = test_user_lb.remote
        assert remote_url

        sally_lb = LabBook(mock_config_file[0])
        sally_lb.from_remote(remote_url, username="sally", owner="default", labbook_name="labbook1")
        assert sally_lb.active_branch == "gm.workspace-sally"
        sally_lb.makedir(relative_path='code/sally-dir', create_activity_record=True)
        sally_lb.sync('sally')

        sync_query = """
        mutation x {
            syncLabbook(input: {
                labbookName: "labbook1",
                owner: "default"
            }) {
                updateCount
            }
        }
        """
        r = fixture_working_dir[2].execute(sync_query, context_value=req)

        assert 'errors' not in r
        assert r['data']['syncLabbook']['updateCount'] == 6
        assert test_user_lb.active_branch == 'gm.workspace-default'

        c = test_user_lb.sync('default')
        assert c == 0
