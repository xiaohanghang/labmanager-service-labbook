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
import multiprocessing
import os
import pprint
import pytest
import shutil
import tempfile
import threading
import time
import uuid

import graphene
from mock import patch
import requests

from lmcommon.environment import ComponentManager, RepositoryManager
from lmcommon.dispatcher import Dispatcher, JobKey
from lmcommon.labbook import LabBook
from lmsrvlabbook.api.mutation import LabbookMutations
from lmsrvlabbook.api.query import LabbookQuery
from lmsrvlabbook.tests.fixtures import fixture_working_dir_env_repo_scoped, fixture_working_dir
from lmcommon.fixtures import ENV_UNIT_TEST_REPO, ENV_UNIT_TEST_BASE, ENV_UNIT_TEST_REV


import service


@pytest.fixture()
def start_server():
    pass


class SampleMockObject(object):
    def method_to_mock(self):
        with open('/tmp/cats', 'w') as f:
            f.write("If you see this file, things didn't work")


def mocky(self):
    with open('/tmp/dogs', 'w') as f:
        f.write("This indicates the mocking in a subprocess worked!")


def invoker():
    return SampleMockObject().method_to_mock()

@pytest.fixture(scope="session")
def pause():
    time.sleep(3)

class TestLabbookMutation(object):

    def test_mocking_in_subprocess(self):
        # This test should remain to validate that mocking applies to classes
        # loaded by a sub-process of this pytest process.
        if os.path.exists('/tmp/cats'):
            os.remove('/tmp/cats')
        if os.path.exists('/tmp/dogs'):
            os.remove('/tmp/dogs')
        with patch.object(SampleMockObject, 'method_to_mock', mocky):
            assert not os.path.exists('/tmp/cats')
            proc = multiprocessing.Process(target=invoker)
            proc.daemon = True
            proc.start()
            time.sleep(1)
            assert not os.path.exists('/tmp/cats')
            assert os.path.exists('/tmp/dogs')


    def test_launch_api_server(self, pause, fixture_working_dir_env_repo_scoped):
        proc = multiprocessing.Process(target=service.main, kwargs={'debug': False})
        proc.daemon = True
        proc.start()

        time.sleep(4)
        assert proc.is_alive()
        proc.terminate()


    def test_insert_file(self, fixture_working_dir_env_repo_scoped):
        # TODO - Pending on integration tests working.
        pass

    def test_export_and_import_lb(self, fixture_working_dir_env_repo_scoped):

        api_server_proc = multiprocessing.Process(target=service.main, kwargs={'debug': False})
        api_server_proc.daemon = True
        api_server_proc.start()
        assert api_server_proc.is_alive()
        time.sleep(5)
        assert api_server_proc.is_alive()

        # Make and validate request
        assert api_server_proc.is_alive()

        lb_name = "mutation-export-import-unittest"
        lb = LabBook(fixture_working_dir_env_repo_scoped[0])
        lb.new(name=lb_name, description="Import/Export Mutation Testing.",
               owner={"username": "default"})
        cm = ComponentManager(lb)
        cm.add_component("base", ENV_UNIT_TEST_REPO, 'ut-busybox', 0)

        assert api_server_proc.is_alive()
        export_query = """
        mutation export {
          exportLabbook(input: {
            owner: "default",
            labbookName: "%s"
          }) {
            jobKey
          }
        }
        """ % lb.name
        r = fixture_working_dir_env_repo_scoped[2].execute(export_query)
        pprint.pprint(r)

        # Sleep while the background job completes, and then delete new lb.
        time.sleep(5)
        d = Dispatcher()
        job_status = d.query_task(JobKey(r['data']['exportLabbook']['jobKey']))

        # Delete existing labbook in file system.
        shutil.rmtree(lb.root_dir)
        assert api_server_proc.is_alive()

        assert job_status.status == 'finished'
        assert not os.path.exists(lb.root_dir)
        assert os.path.exists(job_status.result)
        pprint.pprint(job_status.result)

        if os.path.exists(os.path.join('/tmp', os.path.basename(job_status.result))):
            os.remove(os.path.join('/tmp', os.path.basename(job_status.result)))
        new_path = shutil.move(job_status.result, '/tmp')

        # Now, import the labbook that was just exported.
        export_query = """
        mutation import {
          importLabbook(input: {
          }) {
            jobKey
          }
        }
        """

        files = {'uploadFile': open(new_path, 'rb')}
        qry = {"query": export_query}
        assert api_server_proc.is_alive()
        r = requests.post('http://localhost:10001/labbook/', data=qry, files=files)

        time.sleep(0.5)
        pprint.pprint(r)
        assert 'errors' not in r
        time.sleep(2)

