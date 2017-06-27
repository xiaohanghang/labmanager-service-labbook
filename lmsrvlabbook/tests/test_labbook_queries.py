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

from lmcommon.labbook import LabBook
from lmcommon.configuration import Configuration

from ..api import LabbookMutations, LabbookQueries


# Create ObjectType clases, since the LabbookQueries and LabbookMutations are abstract (allowing multiple inheritance)
class Query(LabbookQueries, graphene.ObjectType):
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


class TestLabBookServiceQueries(object):
    def test_list_users(self, mock_config_file, snapshot):
        """Test listing users"""
        # Create labbooks
        lb = LabBook(mock_config_file[0])
        lb.new(username="test1", owner={"username": "test1"}, name="labbook1", description="my first labbook")
        lb.new(username="test2", owner={"username": "test2"}, name="labbook1", description="my first labbook")
        lb.new(username="test3", owner={"username": "test3"}, name="labbook1", description="my first labbook")

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            # Make and validate request
            client = Client(mock_config_file[2])

            query = """
            {
              users {
                username
              }
            }
            """

            snapshot.assert_match(client.execute(query))

    def test_list_labbooks(self, mock_config_file, snapshot):
        """Test listing labbooks"""
        # Create labbooks
        lb = LabBook(mock_config_file[0])
        lb.new(username="default", owner={"username": "default"}, name="labbook1", description="my first labbook1")
        lb.new(username="default", owner={"username": "default"}, name="labbook2", description="my first labbook2")
        lb.new(username="test3", owner={"username": "test3"}, name="labbook2", description="my first labbook3")

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            # Make and validate request
            client = Client(mock_config_file[2])

            # Get LabBooks for the "logged in user" - Currently just "default"
            query = """
            {
              labbooks{
                name                
                description
              }
            }
            """
            snapshot.assert_match(client.execute(query))

    def test_get_labbook(self, mock_config_file, snapshot):
        """Test listing labbooks"""
        # Create labbooks
        lb = LabBook(mock_config_file[0])
        lb.new(username="default", name="labbook1", description="my first labbook1")

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            # Make and validate request
            client = Client(mock_config_file[2])

            # Get LabBooks for a single user - Don't get the ID field since it is a UUID
            query = """
            {
              labbook(name: "labbook1") {
                name
                description
                localBranches
                remoteBranches
              }
            }
            """
            snapshot.assert_match(client.execute(query))

            # Test selecting a single parameter
            query = """
            {
              labbook(name: "labbook1") {
                name
              }
            }
            """
            snapshot.assert_match(client.execute(query))

    def test_get_multiple(self, mock_config_file, snapshot):
        """Test hitting multiple queries at once"""
        # Create labbooks
        lb = LabBook(mock_config_file[0])
        lb.new(username="default", name="a-test-labbook", description="a different description!<>;")
        lb.new(username="default", name="asdf", description="fghghfjghgf3454dfs dsfasf f sfsadf asdf asdf sda")
        lb.new(username="tester", name="sjdf932sDJFj-df-sdfasj", description="fgdhdfasdf")

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            # Make and validate request
            client = Client(mock_config_file[2])

            # Get LabBooks for a single user - Don't get the ID field since it is a UUID
            query = """
            {
              labbook(name: "a-test-labbook") {    
                name
                description
              }
              users{
                username
              }
              labbooks {
                name                
                description
              }
            }
            """
            snapshot.assert_match(client.execute(query))
