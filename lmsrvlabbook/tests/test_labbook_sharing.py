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
import tempfile
import datetime
import pprint
from zipfile import ZipFile
from pkg_resources import resource_filename
import getpass

from snapshottest import snapshot
from lmsrvlabbook.tests.fixtures import fixture_working_dir_env_repo_scoped, fixture_working_dir, _create_temp_work_dir

import pytest
from graphene.test import Client
from mock import patch
from werkzeug.datastructures import FileStorage

from lmcommon.configuration import Configuration
from lmcommon.dispatcher.jobs import export_labbook_as_zip
from lmcommon.fixtures import remote_labbook_repo, mock_config_file
from lmcommon.labbook import LabBook


@pytest.fixture()
def mock_create_labbooks(fixture_working_dir):
    # Create a labbook in the temporary directory
    lb = LabBook(fixture_working_dir[0])
    lb.new(owner={"username": "default"}, name="sample-repo-lb", description="Cats labbook 1")

    # Create a file in the dir
    with open(os.path.join(fixture_working_dir[1], 'codefile.c'), 'w') as sf:
        sf.write("1234567")
        sf.seek(0)
    lb.insert_file('code', sf.name, '')

    assert os.path.isfile(os.path.join(lb.root_dir, 'code', 'codefile.c'))
    # name of the config file, temporary working directory, the schema
    yield fixture_working_dir, lb


class TestLabbookSharing(object):
    def test_import_remote_labbook(self, remote_labbook_repo, fixture_working_dir):
        client = Client(fixture_working_dir[2])

        query = f"""
        mutation importFromRemote {{
          importRemoteLabbook(
            input: {{
              owner: "test",
              labbookName: "sample-repo-lb",
              remoteUrl: "{remote_labbook_repo}"
            }}) {{
              activeBranch
            }}
        }}
        """
        r = client.execute(query)
        # We might not always want to use master as the default branch, but keep it here for now.
        assert r['data']['importRemoteLabbook']['activeBranch'] == 'gm.workspace-default'

        ## Now we want to validate that when we import a labbook from a remote url, we also track the default branch.
        list_all_branches_q = f"""
        {{
            labbook(name: "sample-repo-lb", owner: "test") {{
                branches {{
                    edges {{
                        node {{
                            prefix
                            name
                        }}
                    }}
                }}
            }}
        }}
        """
        r = client.execute(list_all_branches_q)
        nodes = r['data']['labbook']['branches']['edges']
        for n in [x['node'] for x in nodes]:
            # Make sure that the user's local branch was created
            if n['prefix'] is None and n['name'] == 'gm.workspace-default':
                break
        else:
            assert False

        for n in [x['node'] for x in nodes]:
            # Make sure that origin/gm.workspace is in list of branches. This means it tracks.
            if n['prefix'] == 'origin' and n['name'] == 'gm.workspace':
                break
        else:
            assert False

        # Make sure the labbook cloned into the correct directory
        assert os.path.exists(os.path.join(fixture_working_dir[1], 'default', 'test', 'labbooks', 'sample-repo-lb'))

        # Now do a quick test for default_remote
        get_default_remote_q = f"""
        {{
            labbook(name: "sample-repo-lb", owner: "test") {{
                defaultRemote
            }}
        }}
        """
        r = client.execute(get_default_remote_q)
        assert r['data']['labbook']['defaultRemote'] == remote_labbook_repo
        assert 'errors' not in r

    def test_import_remote_labbook_from_same_user(self, remote_labbook_repo, fixture_working_dir):
        # Create a labbook by the "default" user
        conf_file, working_dir = _create_temp_work_dir()
        lb = LabBook(conf_file)
        labbook_dir = lb.new(username="default", name="default-owned-repo-lb", description="my first labbook",
                             owner={"username": "default"})
        lb.checkout_branch("gm.workspace")

        client = Client(fixture_working_dir[2])

        query = f"""
        mutation importFromRemote {{
          importRemoteLabbook(
            input: {{
              owner: "default",
              labbookName: "default-owned-repo-lb",
              remoteUrl: "{labbook_dir}"
            }}) {{
              activeBranch
            }}
        }}
        """
        r = client.execute(query)
        # We might not always want to use master as the default branch, but keep it here for now.
        assert r['data']['importRemoteLabbook']['activeBranch'] == 'gm.workspace-default'

        ## Now we want to validate that when we import a labbook from a remote url, we also track the default branch.
        list_all_branches_q = f"""
        {{
            labbook(name: "default-owned-repo-lb", owner: "default") {{
                branches {{
                    edges {{
                        node {{
                            prefix
                            name
                        }}
                    }}
                }}
            }}
        }}
        """
        r = client.execute(list_all_branches_q)
        nodes = r['data']['labbook']['branches']['edges']
        for n in [x['node'] for x in nodes]:
            # Make sure that origin/master is in list of branches. This means it tracks.
            if n['prefix'] == 'origin' and n['name'] == 'gm.workspace':
                break
        else:
            assert False

        # Make sure the labbook cloned into the correct directory
        assert os.path.exists(os.path.join(fixture_working_dir[1], 'default', 'default', 'labbooks',
                                           'default-owned-repo-lb'))

        # Now do a quick test for default_remote
        get_default_remote_q = f"""
        {{
            labbook(name: "default-owned-repo-lb", owner: "default") {{
                defaultRemote
            }}
        }}
        """
        r = client.execute(get_default_remote_q)
        assert r['data']['labbook']['defaultRemote'] == labbook_dir
        assert 'errors' not in r

    def test_can_checkout_branch(self, mock_create_labbooks, remote_labbook_repo, fixture_working_dir):
        """Test whether there are uncommitted changes or anything that would prevent
        having a fresh branch checked out. """

        f_dir, lb = mock_create_labbooks

        client = Client(fixture_working_dir[2])
        query = f"""
        {{
            labbook(name: "sample-repo-lb", owner: "default") {{
                isRepoClean
            }}
        }}
        """
        r = client.execute(query)
        assert r['data']['labbook']['isRepoClean'] is True

        os.remove(os.path.join(lb.root_dir, 'code', 'codefile.c'))

        r = client.execute(query)
        # We back-door deleted a file in the LB. The repo should now be unclean - prove it.
        assert r['data']['labbook']['isRepoClean'] is False