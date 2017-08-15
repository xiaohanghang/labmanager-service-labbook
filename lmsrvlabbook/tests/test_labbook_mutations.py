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
import uuid
import shutil
from snapshottest import snapshot

from graphene.test import Client
import graphene
from mock import patch

from lmcommon.configuration import Configuration

from lmsrvlabbook.api.mutation import LabbookMutations
from lmsrvlabbook.api.query import LabbookQuery


# Create ObjectType clases, since the LabbookQueries and LabbookMutations are abstract (allowing multiple inheritance)
class Query(LabbookQuery, graphene.ObjectType):
    pass


class Mutation(LabbookMutations, graphene.ObjectType):
    pass


@pytest.fixture()
def mock_config_file():
    """A pytest fixture that creates a temporary directory and a config file to match. Deletes directory after test"""
    # Create a temporary working directory
    temp_dir = os.path.join(tempfile.tempdir, uuid.uuid4().hex)
    os.makedirs(temp_dir)

    with tempfile.NamedTemporaryFile(mode="wt") as fp:
        # Write a temporary config file
        fp.write("""core:
  team_mode: false 
git:
  backend: 'filesystem'
  working_directory: '{}'""".format(temp_dir))
        fp.seek(0)

        # Create test client
        schema = graphene.Schema(query=Query,
                                 mutation=Mutation)

        yield fp.name, temp_dir, schema  # name of the config file, temporary working directory, the schema

    # Remove the temp_dir
    shutil.rmtree(temp_dir)


class TestLabBookServiceMutations(object):
    def test_create_labbook(self, mock_config_file, snapshot):
        """Test listing labbooks"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            # Make and validate request
            client = Client(mock_config_file[2])

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

    def test_create_labbook_already_exists(self, mock_config_file, snapshot):
        """Test listing labbooks"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            # Make and validate request
            client = Client(mock_config_file[2])

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

    def test_create_branch(self, mock_config_file, snapshot):
        """Test creating a new branch in a labbook"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            # Make and validate request
            client = Client(mock_config_file[2])

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

    def test_checkout_branch(self, mock_config_file, snapshot):
        """Test checking out a new branch in a labbook"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            # Make and validate request
            client = Client(mock_config_file[2])

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
            variables = {"labbook_name": "test-lab-book3", "branch_name": "dev-branch-5"}

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