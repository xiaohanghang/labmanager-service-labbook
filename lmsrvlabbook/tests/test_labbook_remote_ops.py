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
import responses
from lmcommon.labbook import LabBook

from snapshottest import snapshot
from lmsrvlabbook.tests.fixtures import fixture_working_dir

import pytest


class TestLabBookRemoteOperations(object):

    def test_delete_remote_labbook_dryrun(self, fixture_working_dir):
        """Test deleting a LabBook on a remote server - dry run"""

        delete_query = f"""
        mutation delete {{
            deleteRemoteLabbook(input: {{
                owner: "default",
                labbookName: "new-labbook",
                confirm: false
            }}) {{
                success
            }}
        }}
        """
        r = fixture_working_dir[2].execute(delete_query)
        print(r)
        assert 'errors' not in r
        assert r['data']['deleteRemoteLabbook']['success'] is False

    @responses.activate
    def test_delete_remote_labbook(self, fixture_working_dir):
        """Test deleting a LabBook on a remote server"""
        # Setup responses mock for this test
        responses.add(responses.GET, 'https://usersrv.gigantum.io/key',
                      json={'key': 'afaketoken'}, status=200)
        responses.add(responses.GET, 'https://repo.gigantum.io/api/v4/projects/default%2Fnew-labbook',
                      json=[{
                              "id": 27,
                              "description": "",
                            }],
                      status=200)
        responses.add(responses.DELETE, 'https://repo.gigantum.io/api/v4/projects/default%2Fnew-labbook',
                      json={
                                "message": "202 Accepted"
                            },
                      status=202)
        responses.add(responses.GET, 'https://repo.gigantum.io/api/v4/projects/default%2Fnew-labbook',
                      json=[{
                                "message": "404 Project Not Found"
                            }],
                      status=404)

        delete_query = f"""
        mutation delete {{
            deleteRemoteLabbook(input: {{
                owner: "default",
                labbookName: "new-labbook",
                confirm: true
            }}) {{
                success
            }}
        }}
        """
        r = fixture_working_dir[2].execute(delete_query)
        assert 'errors' not in r
        assert r['data']['deleteRemoteLabbook']['success'] is True

        # Try deleting again, which should return an eror
        r = fixture_working_dir[2].execute(delete_query)
        assert 'errors' in r
        assert r['errors'][0]['message'] == 'Cannot remove remote repository that does not exist'

    @responses.activate
    def test_list_remote_labbooks_az(self, fixture_working_dir, snapshot):
        """test list labbooks"""
        lb = LabBook(fixture_working_dir[0])
        lb.new(username='default', owner={"username": "testuser"}, name="test11", description="my first labbook1")

        responses.add(responses.GET, 'https://usersrv.gigantum.io/key',
                      json={'key': 'afaketoken'}, status=200)
        dummy_data = [
                        {
                            "id": 118,
                            "name": "test11",
                            "name_with_namespace": "testuser / test11",
                            "path_with_namespace": "testuser/test11",
                            "created_at": "2018-04-19T19:06:11.009Z",
                            "last_activity_at": "2018-04-19T22:08:05.974Z",
                            "visibility": "private",
                            "owner": {
                                "id": 14,
                                "name": "testuser",
                                "username": "testuser",
                                "state": "active",
                            },
                            "creator_id": 14,
                            "namespace": {
                                "id": 14,
                                "name": "testuser",
                                "path": "testuser",
                                "kind": "user",
                                "full_path": "testuser"
                            },
                            "import_status": "none",
                            "permissions": {
                                "project_access": {
                                    "access_level": 30,
                                    "notification_level": 3
                                },
                            }
                        },
                        {
                            "id": 138,
                            "name": "test2",
                            "name_with_namespace": "testuser / test2",
                            "path_with_namespace": "testuser/test2",
                            "created_at": "2018-04-19T19:36:11.009Z",
                            "last_activity_at": "2018-04-19T20:58:05.974Z",
                            "visibility": "private",
                            "owner": {
                                "id": 14,
                                "name": "testuser",
                                "username": "testuser",
                                "state": "active",
                            },
                            "creator_id": 14,
                            "namespace": {
                                "id": 14,
                                "name": "testuser",
                                "path": "testuser",
                                "kind": "user",
                                "full_path": "testuser"
                            },
                            "import_status": "none",
                            "permissions": {
                                "project_access": {
                                    "access_level": 30,
                                    "notification_level": 3
                                },
                            }
                        }]

        responses.add(responses.GET, 'https://repo.gigantum.io/api/v4/projects/',
                      json=dummy_data, status=200)

        list_query = """
                    {
                    labbookList{
                      remoteLabbooks(sort: "az", reverse: false){
                        edges{
                          node{
                            id
                            description
                            creationDateUtc
                            modifiedDateUtc
                            name
                            owner
                            isLocal
                          }
                          cursor
                        }
                        pageInfo{
                          hasNextPage
                        }
                      }
                    }
                    }"""

        r = fixture_working_dir[2].execute(list_query)
        print(r)
        assert 'errors' not in r
        snapshot.assert_match(r)

        list_query = """
                    {
                    labbookList{
                      remoteLabbooks(sort: "modified_on", reverse: false){
                        edges{
                          node{
                            id
                            description
                            creationDateUtc
                            modifiedDateUtc
                            name
                            owner
                          }
                          cursor
                        }
                        pageInfo{
                          hasNextPage
                        }
                      }
                    }
                    }"""

        r = fixture_working_dir[2].execute(list_query)
        assert 'errors' not in r
        snapshot.assert_match(r)
