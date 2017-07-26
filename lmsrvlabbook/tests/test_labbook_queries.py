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

from ..api import LabbookMutations, LabbookQuery


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

def create_labbooks(lb: LabBook):
    lb.new(owner={"username": "default"}, name="labbook1", description="Cats labbook 1")
    lb.new(owner={"username": "default"}, name="labbook2", description="Dogs labbook 2")
    lb.new(owner={"username": "default"}, name="labbook3", description="Mice labbook 3")
    lb.new(owner={"username": "default"}, name="labbook4", description="Horses labbook 4")
    lb.new(owner={"username": "default"}, name="labbook5", description="Cheese labbook 5")
    lb.new(owner={"username": "default"}, name="labbook6", description="Goat labbook 6")
    lb.new(owner={"username": "default"}, name="labbook7", description="Turtle labbook 7")
    lb.new(owner={"username": "default"}, name="labbook8", description="Lamb labbook 8")
    lb.new(owner={"username": "default"}, name="labbook9", description="Taco labbook 9")
    lb.new(owner={"username": "test3"}, name="labbook-0", description="This should not show up.")


class TestLabBookServiceQueries(object):
    # def test_list_users(self, mock_config_file, snapshot):
    #     """Test listing users"""
    #     # Create labbooks
    #     lb = LabBook(mock_config_file[0])
    #     lb.new(owner={"username": "test1"}, name="labbook1", description="my first labbook")
    #     lb.new(owner={"username": "test2"}, name="labbook1", description="my first labbook")
    #     lb.new(owner={"username": "test3"}, name="labbook1", description="my first labbook")
    #
    #     # Mock the configuration class it it returns the same mocked config file
    #     with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
    #         # Make and validate request
    #         client = Client(mock_config_file[2])
    #
    #         query = """
    #         {
    #           users {
    #             username
    #           }
    #         }
    #         """
    #
    #         snapshot.assert_match(client.execute(query))

    def test_list_labbooks(self, mock_config_file, snapshot):
        """Test listing labbooks"""

        lb = LabBook(mock_config_file[0])
        lb.new(owner={"username": "default"}, name="labbook1", description="my first labbook1")
        lb.new(owner={"username": "default"}, name="labbook2", description="my first labbook2")
        lb.new(owner={"username": "test3"}, name="labbook2", description="my first labbook3")

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            # Make and validate request
            client = Client(mock_config_file[2])

            # Get LabBooks for the "logged in user" - Currently just "default"
            query = """
            {
                localLabbooks {
                    edges {
                        node {
                            name
                            description
                        }
                        cursor
                    }
                }
            }
            """
            snapshot.assert_match(client.execute(query))

    def test_pagination_noargs(self, mock_config_file, snapshot):
        lb = LabBook(mock_config_file[0])
        create_labbooks(lb)

        # Mock the configuration class it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            client = Client(mock_config_file[2])
            query = """
                    {
                        localLabbooks {
                            edges {
                                node {
                                    name
                                    description
                                }
                                cursor
                            }
                            pageInfo {
                                hasNextPage
                                hasPreviousPage
                            }
                        }
                    }
                    """
            snapshot.assert_match(client.execute(query))

    def test_pagination_first_only(self, mock_config_file, snapshot):
        lb = LabBook(mock_config_file[0])
        create_labbooks(lb)

        # Mock the configuration class it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            client = Client(mock_config_file[2])
            query = """
                    {
                        localLabbooks(first: 3) {
                            edges {
                                node {
                                    name
                                    description
                                }
                                cursor
                            }
                            pageInfo {
                                hasNextPage
                                hasPreviousPage
                            }
                        }
                    }
                    """
            snapshot.assert_match(client.execute(query))

    def test_pagination_first_and_after(self, mock_config_file, snapshot):
        lb = LabBook(mock_config_file[0])
        create_labbooks(lb)

        # Nominal case
        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            client = Client(mock_config_file[2])
            query = """
                    {
                        localLabbooks(first: 4, after: "Mg==") {
                            edges {
                                node {
                                    name
                                    description
                                }
                                cursor
                            }
                            pageInfo {
                                hasNextPage
                                hasPreviousPage
                            }
                        }
                    }
                    """
            snapshot.assert_match(client.execute(query))

            # Overrunning end of list of labbooks
            query = """
                    {
                        localLabbooks(first: 6, after: "Ng==") {
                            edges {
                                node {
                                    name
                                    description
                                }
                                cursor
                            }
                            pageInfo {
                                hasNextPage
                                hasPreviousPage
                            }
                        }
                    }
                    """
            snapshot.assert_match(client.execute(query))

            # Overrunning end of list of labbooks, returns empty set.
            query = """
                    {
                        localLabbooks(first: 6, after: "OA==") {
                            edges {
                                node {
                                    name
                                    description
                                }
                                cursor
                            }
                            pageInfo {
                                hasNextPage
                                hasPreviousPage
                            }
                        }
                    }
                    """
            snapshot.assert_match(client.execute(query))

    def test_pagination_last_only(self, mock_config_file, snapshot):
        lb = LabBook(mock_config_file[0])
        create_labbooks(lb)

        # Mock the configuration class it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            client = Client(mock_config_file[2])
            query = """
                    {
                        localLabbooks(last: 3) {
                            edges {
                                node {
                                    name
                                    description
                                }
                                cursor
                            }
                            pageInfo {
                                hasNextPage
                                hasPreviousPage
                            }
                        }
                    }
                    """
            snapshot.assert_match(client.execute(query))

    def test_pagination_last_and_before(self, mock_config_file, snapshot):
        lb = LabBook(mock_config_file[0])
        create_labbooks(lb)

        # Mock the configuration class it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            client = Client(mock_config_file[2])
            query = """
                    {
                        localLabbooks(last: 3, before: "Nw==") {
                            edges {
                                node {
                                    name
                                    description
                                }
                                cursor
                            }
                            pageInfo {
                                hasNextPage
                                hasPreviousPage
                            }
                        }
                    }
                    """
            snapshot.assert_match(client.execute(query))

            # Overrun start of list
            query = """
                    {
                        localLabbooks(last: 3, before: "MQ==") {
                            edges {
                                node {
                                    name
                                    description
                                }
                                cursor
                            }
                            pageInfo {
                                hasNextPage
                                hasPreviousPage
                            }
                        }
                    }
                    """
            snapshot.assert_match(client.execute(query))

            # Overrun with no intersection (should return empty list)
            query = """
                    {
                        localLabbooks(last: 3, before: "MA==") {
                            edges {
                                node {
                                    name
                                    description
                                }
                                cursor
                            }
                            pageInfo {
                                hasNextPage
                                hasPreviousPage
                            }
                        }
                    }
                    """
            snapshot.assert_match(client.execute(query))

    def test_pagination(self, mock_config_file, snapshot):
        """Test pagination and cursors"""

        lb = LabBook(mock_config_file[0])
        create_labbooks(lb)

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            # Make and validate request
            client = Client(mock_config_file[2])

            # Get LabBooks for the "logged in user" - Currently just "default"
            query = """
                    {
                        localLabbooks(first: 2, after: "MQ==") {
                            edges {
                                node {
                                    name
                                    description
                                }
                                cursor
                            }
                            pageInfo {
                                hasNextPage
                                hasPreviousPage
                            }
                        }
                    }
                    """
            snapshot.assert_match(client.execute(query))

            before_query = """
                    {
                        localLabbooks(last: 2, before: "Ng==") {
                            edges {
                                node {
                                    name
                                    description
                                }
                                cursor
                            }
                            pageInfo {
                                hasNextPage
                                hasPreviousPage
                            }
                        }
                    }
                    """
            snapshot.assert_match(client.execute(before_query))

    def test_get_labbook(self, mock_config_file, snapshot):
        """Test listing labbooks"""
        # Create labbooks
        lb = LabBook(mock_config_file[0])
        lb.new(owner={"username": "default"}, name="labbook1", description="my first labbook1")

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            # Make and validate request
            client = Client(mock_config_file[2])

            # Get LabBooks for a single user - Don't get the ID field since it is a UUID
            query = """
            {
              labbook(name: "labbook1", owner: "default") {
                name
                description
                activeBranch {
                    name
                }
              }
            }
            """
            snapshot.assert_match(client.execute(query))
