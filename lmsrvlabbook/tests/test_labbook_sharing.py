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
from lmsrvlabbook.tests.fixtures import fixture_working_dir_env_repo_scoped, fixture_working_dir

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
    with open(os.path.join(fixture_working_dir[1], 'sillyfile'), 'w') as sf:
        sf.write("1234567")
        sf.seek(0)
    lb.insert_file(sf.name, 'code')

    assert os.path.isfile(os.path.join(lb.root_dir, 'code', 'sillyfile'))
    # name of the config file, temporary working directory, the schema
    yield fixture_working_dir, lb

class TestLabbookSharing(object):
    def test_import_remote_labbook(self, remote_labbook_repo, fixture_working_dir):
        client = Client(fixture_working_dir[2])

        query = f"""
        mutation importFromRemote {{
          importRemoteLabbook(
            input: {{
              owner: "default",
              labbookName: "sample-repo-lb",
              remoteUrl: "{remote_labbook_repo}"
            }}) {{
              activeBranch
            }}
        }}
        """
        r = client.execute(query)
        # We might not always want to use master as the default branch, but keep it here for now.
        assert r['data']['importRemoteLabbook']['activeBranch'] == 'master'

        ## Now we want to validate that when we import a labbook from a remote url, we also track the default branch.
        list_all_branches_q = f"""
        {{
            labbook(name: "sample-repo-lb", owner: "default") {{
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
            if n['prefix'] == 'origin' and n['name'] == 'master':
                break
        else:
            assert False


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

        os.remove(os.path.join(lb.root_dir, 'code', 'sillyfile'))

        r = client.execute(query)
        # We back-door deleted a file in the LB. The repo should now be unclean - prove it.
        assert r['data']['labbook']['isRepoClean'] is False

    def test_pull_from_remote_and_push_back_something_new(self, mock_create_labbooks, mock_config_file,
                                                          remote_labbook_repo, fixture_working_dir):
        f_dir, lb = mock_create_labbooks

        client = Client(fixture_working_dir[2])

        ## ADD A REMOTE
        add_labbook_remote_git_q = f"""
        mutation X {{
            addLabbookRemote(input: {{
                labbookName: "sample-repo-lb",
                owner: "default",
                remoteName: "origin",
                remoteUrl: "{remote_labbook_repo}"
            }}) {{
                success
            }}
        }}
        """
        r = client.execute(add_labbook_remote_git_q)
        pprint.pprint(r)
        assert not 'errors' in r
        assert 'data' in r
        assert r['data']['addLabbookRemote']['success'] is True

        ## CREATE A NEW BRANCH FOR NEW WORK
        create_new_branch_q = f"""
        mutation X {{
            createBranch(input: {{
                labbookName: "sample-repo-lb",
                owner: "default",
                branchName: "new-branch-from-mutation"
            }}) {{
                branch {{
                    name
                }}
            }}
        }}          
        """
        r = client.execute(create_new_branch_q)
        pprint.pprint("CreateBranch")
        pprint.pprint(r)
        assert not 'errors' in r
        assert r['data']['createBranch']['branch']['name'] == 'new-branch-from-mutation'
        assert lb.active_branch == 'new-branch-from-mutation'
        lb.delete_file('code', 'codefile.c')

        ## PUSH BRANCH TO REMOTE
        push_branch_q = f"""
        mutation X {{
            pushActiveBranchToRemote(input: {{
                labbookName: "sample-repo-lb",
                owner: "default"
            }}) {{
                success
            }}
        }} 
        """
        r = client.execute(push_branch_q)
        assert 'errors' not in r
        assert r['data']['pushActiveBranchToRemote']['success'] is True

        # Reconstruct the remote lab book so we can list its branches.
        remote_lb = LabBook(mock_config_file[0])
        remote_lb.from_directory(remote_labbook_repo)
        # Ensure branch now exists on remote, as a local branch.
        assert 'new-branch-from-mutation' in remote_lb.get_branches()['local']

        ## PULL ACTIVE BRANCH FROM REMOTE
        pull_query = f"""
        mutation P {{
            pullActiveBranchFromRemote(input: {{
                labbookName: "sample-repo-lb",
                owner: "default"
            }}) {{
                success
            }}
        }}        
        """
        r = client.execute(pull_query)
        pprint.pprint("PullQuery")
        pprint.pprint(r)
        assert not 'errors' in r
        assert r['data']['pullActiveBranchFromRemote']['success'] is True

        ## ENUMERATE AND LIST ALL BRANCHES
        list_all_branches_q = f"""
        {{
            labbook(name: "sample-repo-lb", owner: "default") {{
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
        pprint.pprint(r)

        ## CHECKOUT (REMOTE) BRANCH
        checkout_remote_branch_q = f"""
        mutation X {{
            checkoutBranch(input: {{
                labbookName: "sample-repo-lb",
                owner: "default",
                branchName: "testing-branch"
            }}) {{
                labbook {{
                    name
                    activeBranch {{
                        name
                    }}
                }}
            }}
        }}
        """
        r = client.execute(checkout_remote_branch_q)
        pprint.pprint(r)
        assert not 'errors' in r
        assert r['data']['checkoutBranch']['labbook']['activeBranch']['name'] == 'testing-branch'
        assert os.path.exists(os.path.join(lb.root_dir, 'code', 'codefile.c'))

        ### CHECKOUT BRANCH WITH WORK CREATED AT BEGINNING AGAIN AND RESTORE IT
        checkout_branch_q = f"""
        mutation X {{
            checkoutBranch(input: {{
                labbookName: "sample-repo-lb",
                owner: "default",
                branchName: "new-branch-from-mutation"
            }}) {{
                labbook {{
                    activeBranch {{
                        name
                    }}
                }}
            }}
        }}        
        """
        r = client.execute(checkout_branch_q)
        pprint.pprint("CheckoutBranch")
        pprint.pprint(r)
        assert not 'errors' in r
        assert r['data']['checkoutBranch']['labbook']['activeBranch']['name'] == 'new-branch-from-mutation'
        # Remember, in this branch we deleted codefile.c, but not in testing-branch.
        assert not os.path.exists(os.path.join(lb.root_dir, 'code', 'codefile.c'))