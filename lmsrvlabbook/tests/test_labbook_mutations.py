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
from lmsrvlabbook.tests.fixtures import fixture_working_dir_env_repo_scoped, fixture_working_dir

from graphene.test import Client
import graphene
from mock import patch
import requests

from lmcommon.configuration import Configuration
from lmcommon.dispatcher import Dispatcher, JobKey
from lmcommon.environment import ComponentManager, RepositoryManager
from lmcommon.labbook import LabBook

from lmsrvlabbook.api.mutation import LabbookMutations
from lmsrvlabbook.api.query import LabbookQuery


# Create ObjectType clases, since the LabbookQueries and LabbookMutations are abstract (allowing multiple inheritance)
class Query(LabbookQuery, graphene.ObjectType):
    pass


class Mutation(LabbookMutations, graphene.ObjectType):
    pass


@pytest.fixture()
def mock_create_labbooks(fixture_working_dir):
    # Create a labbook in the temporary directory
    lb = LabBook(fixture_working_dir[0])
    lb.new(owner={"username": "default"}, name="labbook1", description="Cats labbook 1")

    # Create a file in the dir
    with open(os.path.join(fixture_working_dir[1], 'sillyfile'), 'w') as sf:
        sf.write("1234567")
        sf.seek(0)
    lb.insert_file(sf.name, 'code')

    assert os.path.isfile(os.path.join(lb.root_dir, 'code', 'sillyfile'))
    # name of the config file, temporary working directory, the schema
    yield fixture_working_dir


class TestLabBookServiceMutations(object):
    def test_create_labbook(self, fixture_working_dir, snapshot):
        """Test listing labbooks"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir[0]):
            # Make and validate request
            client = Client(fixture_working_dir[2])

            # Create LabBook
            query = """
            mutation myCreateLabbook($name: String!, $desc: String!) {
              createLabbook(input: {name: $name, description: $desc}) {
                labbook {
                  id
                  name
                  description
                }
              }
            }
            """

            variables = {"name": "test-lab-book1", "desc": "my test description"}
            client.execute(query, variable_values=variables)

            # Get LabBook you just created
            query = """
            {
              labbook(name: "test-lab-book1", owner: "default") {
                name
                description
                notes{
                  edges{
                    node{
                      message
                      freeText
                    }
                  }
                }
              }
            }
            """
            snapshot.assert_match(client.execute(query))

    def test_create_labbook_already_exists(self, fixture_working_dir, snapshot):
        """Test listing labbooks"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir[0]):
            # Make and validate request
            client = Client(fixture_working_dir[2])

            # Create LabBook
            query = """
            mutation myCreateLabbook($name: String!, $desc: String!){
              createLabbook(input: {name: $name, description: $desc}){
                labbook{                  
                  name
                  description
                }
              }
            }
            """
            variables = {"name": "test-lab-book", "desc": "my test description"}

            snapshot.assert_match(client.execute(query, variable_values=variables))

            # Second should fail with an error message
            snapshot.assert_match(client.execute(query, variable_values=variables))

    def test_create_branch(self, fixture_working_dir, snapshot):
        """Test creating a new branch in a labbook"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir[0]):
            # Make and validate request
            client = Client(fixture_working_dir[2])

            # Create LabBook
            query = """
            mutation CreateLabBook($name: String!, $desc: String!){
              createLabbook(input: {name: $name, description: $desc}){
                labbook{
                  id
                  name
                  description
                }
              }
            }
            """
            variables = {"name": "test-lab-book2", "desc": "Yada yada blah blah blah 99"}

            client.execute(query, variable_values=variables)

            # Create a Branch
            query = """
            mutation BranchLabBook($labbook_name: String!, $branch_name: String!){
              createBranch(input: {labbookName: $labbook_name, branchName: $branch_name}) {
                branch {
                    name
                }
              }
            }
            """
            variables = {"labbook_name": "test-lab-book2", "branch_name": "dev-branch-1"}

            client.execute(query, variable_values=variables)

            # Create Branch
            query = """
            {
              labbook(name: "test-lab-book2", owner: "default") {
                name
                description
                activeBranch {
                    name
                }
                branches {
                    edges {
                        node {
                            name
                        }
                    }
                }
              }
            }
            """
            snapshot.assert_match(client.execute(query))

    def test_checkout_branch(self, fixture_working_dir, snapshot):
        """Test checking out a new branch in a labbook"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir[0]):
            # Make and validate request
            client = Client(fixture_working_dir[2])

            # Create LabBook
            query = """
            mutation CreateLabBook($name: String!, $desc: String!) {
              createLabbook(input: {name: $name, description: $desc}) {
                labbook {
                  id
                  name
                  description
                }
              }
            }
            """
            variables = {"name": "test-lab-book3", "desc": "a different description"}

            client.execute(query, variable_values=variables)

            # Create a Branch
            query = """
            mutation BranchLabBook($labbook_name: String!, $branch_name: String!) {
              createBranch(input: {labbookName: $labbook_name, branchName: $branch_name}) {
                branch {                  
                  name                 
                }
              }
            }
            """
            variables = {"labbook_name": "test-lab-book3", "branch_name": "dev-branch-5"}

            snapshot.assert_match(client.execute(query, variable_values=variables))

            # Check branch status
            query = """
            {
              labbook(name: "test-lab-book3", owner: "default") {
                name
                description
                branches {
                    edges {
                        node {
                            prefix
                            name
                        }
                    }
                }
                activeBranch {
                    name
                }
              }
            }
            """
            snapshot.assert_match(client.execute(query))

            #  Checkout a Branch
            query = """
            mutation CheckoutLabBook($labbook_name: String!, $branch_name: String!){
              checkoutBranch(input: {labbookName: $labbook_name, branchName: $branch_name}) {
                labbook {
                  name
                  activeBranch {
                    name
                  }
                }
              }
            }
            """
            variables = {
                "labbook_name": "test-lab-book3",
                "branch_name": "dev-branch-5"
            }

            client.execute(query, variable_values=variables)

            # Check branch status
            query = """
            {
              labbook(name: "test-lab-book3", owner: "default") {
                name
                description
                activeBranch {
                  name
                  prefix
                }
              }
            }
            """
            snapshot.assert_match(client.execute(query))

    def test_move_file(self, mock_create_labbooks):
        """Test checking out a new branch in a labbook"""
        with patch.object(Configuration, 'find_default_config', lambda self: mock_create_labbooks[0]):
            client = Client(mock_create_labbooks[2])
            query = """
            mutation MoveLabbookFile {
              moveLabbookFile(
                input: {
                  user: "default",
                  owner: "default",
                  labbookName: "labbook1",
                  srcPath: "code",
                  dstPath: "input"
                }) {
                  success
                }
            }
            """
            res = client.execute(query)
            assert res['data']['moveLabbookFile']['success'] == True

    def test_delete_file(self, mock_create_labbooks):
        with patch.object(Configuration, 'find_default_config', lambda self: mock_create_labbooks[0]):
            client = Client(mock_create_labbooks[2])
            query = """
            mutation deleteLabbookFile {
              deleteLabbookFile(
                input: {
                  user: "default",
                  owner: "default",
                  labbookName: "labbook1",
                  filePath: "code/sillyfile",
                }) {
                  success
                }
            }
            """
            res = client.execute(query)
            assert res['data']['deleteLabbookFile']['success'] == True

    def test_makedir(self, mock_create_labbooks):
        with patch.object(Configuration, 'find_default_config', lambda self: mock_create_labbooks[0]):
            client = Client(mock_create_labbooks[2])
            query = """
            mutation makeLabbookDirectory {
              makeLabbookDirectory(
                input: {
                  user: "default",
                  owner: "default",
                  labbookName: "labbook1",
                  dirName: "output/new_folder",
                }) {
                  success
                }
            }
            """
            res = client.execute(query)
            import pprint; pprint.pprint(res)
            assert res['data']['makeLabbookDirectory']['success'] == True

    def test_insert_file(self, fixture_working_dir):
        # TODO - Pending on integration tests working.
        pass

    # def test_export_and_import_lb(self, fixture_working_dir, snapshot):
    #     with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir[0]):
    #         # Make and validate request
    #         client = Client(fixture_working_dir[2])
    #
    #         lb_name = "mutation-export-import-unittest"
    #         lb = LabBook(fixture_working_dir[0])
    #         lb.new(name=lb_name, description="Import/Export Mutation Testing.",
    #                owner={"username": "test"})
    #         cm = ComponentManager(lb)
    #         cm.add_component("base_image", "gig-dev_environment-components", "gigantum", "ubuntu1604-python3", "0.4")
    #         cm.add_component("dev_env", "gig-dev_environment-components", "gigantum", "jupyter-ubuntu", "0.1")
    #         pprint.pprint(f"NEW TEST LB IN: {lb.root_dir}")
    #
    #         export_query = """
    #         mutation export {
    #           exportLabbook(input: {
    #             user: "test",
    #             owner: "test",
    #             labbookName: "%s"
    #           }) {
    #             jobKey
    #           }
    #         }
    #         """ % lb.name
    #         r = client.execute(export_query)
    #         pprint.pprint(r)
    #
    #         # Sleep while the background job completes, and then delete new lb.
    #         time.sleep(3)
    #         d = Dispatcher()
    #         job_status = d.query_task(JobKey(r['data']['exportLabbook']['jobKey']))
    #
    #         # Delete existing labbook in file system.
    #         shutil.rmtree(lb.root_dir)
    #
    #         assert job_status.status == 'finished'
    #         assert not os.path.exists(lb.root_dir)
    #         assert os.path.exists(job_status.result)
    #         pprint.pprint(job_status.result)
    #
    #         try:
    #             os.remove(job_status.result)
    #         except:
    #             pass
    #
    #             # # Now, import the labbook that was just exported.
    #             # export_query = """
    #             # mutation import {
    #             #   importLabbook(input: {
    #             #     user: "test",
    #             #     owner: "test",
    #             #   }) {
    #             #     jobKey
    #             #   }
    #             # }
    #             # """
    #             #
    #             # files = {'archiveFile': open(job_status.result, 'rb')}
    #             # qry = {"query": export_query}
    #             # r = requests.post('http://localhost:5000/labbook/', data=qry, files=files)
    #             #
    #             # time.sleep(0.5)
    #             # pprint.pprint(r)
    #             # time.sleep(2)
    #             #
    #             # assert False
