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
import tempfile
from werkzeug.datastructures import FileStorage

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

    def test_move_file(self, mock_create_labbooks, snapshot):
        """Test moving a directory"""
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
                  newLabbookFileEdge {
                    node{
                      key
                      isDir
                      size
                    }
                  }
                }
            }
            """
            snapshot.assert_match(client.execute(query))

    def test_move_file_many(self, mock_create_labbooks, snapshot):
        """Test moving a file around a bunch"""
        labbook_dir = os.path.join(mock_create_labbooks[1], 'default', 'default', 'labbooks', 'labbook1')

        with patch.object(Configuration, 'find_default_config', lambda self: mock_create_labbooks[0]):
            client = Client(mock_create_labbooks[2])
            query1 = """
            mutation MoveLabbookFile {
              moveLabbookFile(
                input: {
                  user: "default",
                  owner: "default",
                  labbookName: "labbook1",
                  srcPath: "code/sillyfile",
                  dstPath: "input/sillyfile"
                }) {
                  newLabbookFileEdge {
                    node{
                      key
                      isDir
                      size
                    }
                  }
                }
            }
            """
            query2 = """
            mutation MoveLabbookFile {
              moveLabbookFile(
                input: {
                  user: "default",
                  owner: "default",
                  labbookName: "labbook1",
                  srcPath: "input/sillyfile",
                  dstPath: "code/sillyfile"
                }) {
                  newLabbookFileEdge {
                    node{
                      key
                      isDir
                      size
                    }
                  }
                }
            }
            """
            snapshot.assert_match(client.execute(query1))
            assert os.path.exists(os.path.join(labbook_dir, 'input', 'sillyfile'))
            assert os.path.isfile(os.path.join(labbook_dir, 'input', 'sillyfile'))

            snapshot.assert_match(client.execute(query2))
            assert os.path.exists(os.path.join(labbook_dir, 'code', 'sillyfile'))
            assert os.path.isfile(os.path.join(labbook_dir, 'code', 'sillyfile'))

            snapshot.assert_match(client.execute(query1))
            assert os.path.exists(os.path.join(labbook_dir, 'input', 'sillyfile'))
            assert os.path.isfile(os.path.join(labbook_dir, 'input', 'sillyfile'))

            snapshot.assert_match(client.execute(query2))
            assert os.path.exists(os.path.join(labbook_dir, 'code', 'sillyfile'))
            assert os.path.isfile(os.path.join(labbook_dir, 'code', 'sillyfile'))

            snapshot.assert_match(client.execute(query1))
            assert os.path.exists(os.path.join(labbook_dir, 'input', 'sillyfile'))
            assert os.path.isfile(os.path.join(labbook_dir, 'input', 'sillyfile'))

            snapshot.assert_match(client.execute(query2))
            assert os.path.exists(os.path.join(labbook_dir, 'code', 'sillyfile'))
            assert os.path.isfile(os.path.join(labbook_dir, 'code', 'sillyfile'))

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
            assert res['data']['deleteLabbookFile']['success'] is True

    def test_makedir(self, mock_create_labbooks, snapshot):
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
                  newLabbookFileEdge {
                    node{
                      key
                      isDir
                      size
                    }
                  }
                }}"""
            snapshot.assert_match(client.execute(query))

    def test_add_file(self, mock_create_labbooks, snapshot):
        """Test adding a new file to a labbook"""
        class DummyContext(object):
            def __init__(self, file_handle):
                self.files = {'uploadFile': file_handle}

        client = Client(mock_create_labbooks[2])
        query = """
        mutation addLabbookFile {
          addLabbookFile(
            input: {
              user: "default",
              owner: "default",
              labbookName: "labbook1",
              filePath: "code/myfile.txt",
            }) {
              newLabbookFileEdge {
                node{
                  id
                  key
                  isDir
                  size
                }
              }
            }
        }
        """
        test_file = os.path.join(tempfile.gettempdir(), "myfile.txt")
        with open(test_file, 'wt') as tf:
            tf.write("THIS IS A FILE I MADE!")

        with open(test_file, 'rb') as tf:
            file = FileStorage(tf)

            snapshot.assert_match(client.execute(query, context_value=DummyContext(file)))

            # Check for file
            target_file = os.path.join(mock_create_labbooks[1], 'default', 'default', 'labbooks',
                                       'labbook1', 'code', 'myfile.txt')
            assert os.path.exists(target_file) is True
            assert os.path.isfile(target_file) is True

    def test_add_file_errors(self, mock_create_labbooks, snapshot):
        """Test new file error handling"""
        class DummyContext(object):
            def __init__(self, file_handle):
                self.files = {'uploadFile': file_handle}

        client = Client(mock_create_labbooks[2])
        query = """
        mutation addLabbookFile {
          addLabbookFile(
            input: {
              user: "default",
              owner: "default",
              labbookName: "labbook1",
              filePath: "code/myfile2.txt",
            }) {
                  newLabbookFileEdge {
                    node{
                      key
                      isDir
                      modifiedAt
                      size
                    }
                  }
            }
        }
        """
        test_file = os.path.join(tempfile.gettempdir(), "myfile.txt")
        with open(test_file, 'wt') as tf:
            tf.write("THIS IS A FILE I MADE!")

        with open(test_file, 'rb') as tf:
            file = FileStorage(tf)

            # Fail because no file
            snapshot.assert_match(client.execute(query, context_value=DummyContext(None)))

            # Fail because filenames don't match
            snapshot.assert_match(client.execute(query, context_value=DummyContext(file)))

    def test_add_favorite(self, mock_create_labbooks, snapshot):
        """Method to test adding a favorite"""
        client = Client(mock_create_labbooks[2])

        # Verify no favs
        fav_query = """
                   {
                     labbook(name: "labbook1", owner: "default") {
                       name
                       favorites(subdir: "code") {
                           edges {
                               node {
                                   id
                                   index
                                   key
                                   description
                                   isDir
                               }
                           }
                       }
                     }
                   }
                   """
        snapshot.assert_match(client.execute(fav_query))

        test_file = os.path.join(mock_create_labbooks[1], 'default', 'default', 'labbooks',
                                 'labbook1', 'code', 'test.txt')
        with open(test_file, 'wt') as tf:
            tf.write("a test file...")

        # Add a favorite in code
        query = """
        mutation addFavorite {
          addFavorite(
            input: {
              owner: "default",
              labbookName: "labbook1",
              subdir: "code",
              key: "test.txt",
              description: "my test favorite"
            }) {
              newFavoriteEdge{
                node{
                   id
                   index
                   key
                   description
                   isDir
                   }
              }
            }
        }
        """
        snapshot.assert_match(client.execute(query))

        # Verify the favorite is there
        snapshot.assert_match(client.execute(fav_query))

    def test_add_favorite_at_index(self, mock_create_labbooks, snapshot):
        """Method to test adding a favorite"""
        client = Client(mock_create_labbooks[2])

        # Verify no favs
        fav_query = """
                   {
                     labbook(name: "labbook1", owner: "default") {
                       name
                       favorites(subdir: "code") {
                           edges {
                               node {
                                   id
                                   index
                                   key
                                   description
                                   isDir
                               }
                           }
                       }
                     }
                   }
                   """
        snapshot.assert_match(client.execute(fav_query))

        test_file_root = os.path.join(mock_create_labbooks[1], 'default', 'default', 'labbooks',
                                 'labbook1', 'code')
        with open(os.path.join(test_file_root, 'test1.txt'), 'wt') as tf:
            tf.write("a test file 1")
        with open(os.path.join(test_file_root, 'test2.txt'), 'wt') as tf:
            tf.write("a test file 2")
        with open(os.path.join(test_file_root, 'test3.txt'), 'wt') as tf:
            tf.write("a test file 3")

        # Add a favorite in code
        query = """
        mutation addFavorite {
          addFavorite(
            input: {
              owner: "default",
              labbookName: "labbook1",
              subdir: "code",
              key: "test1.txt",
              description: "my test favorite 1"
            }) {
              newFavoriteEdge{
                node{
                   index
                   key
                   description
                   }
              }
            }
        }
        """
        snapshot.assert_match(client.execute(query))

        query = """
        mutation addFavorite {
          addFavorite(
            input: {
              owner: "default",
              labbookName: "labbook1",
              subdir: "code",
              key: "test2.txt",
              description: "my test favorite 2"
            }) {
              newFavoriteEdge{
                node{
                   index
                   key
                   description
                   }
              }
            }
        }
        """
        snapshot.assert_match(client.execute(query))

        query = """
        mutation addFavorite {
          addFavorite(
            input: {
              owner: "default",
              labbookName: "labbook1",
              subdir: "code",
              key: "test3.txt",
              description: "my test favorite 3",
              index: 1
            }) {
              newFavoriteEdge{
                node{
                   index
                   key
                   description
                   }
              }
            }
        }
        """
        snapshot.assert_match(client.execute(query))

        # Verify the favorites are there
        snapshot.assert_match(client.execute(fav_query))

    def test_delete_favorite(self, mock_create_labbooks, snapshot):
        """Method to test adding a favorite"""
        client = Client(mock_create_labbooks[2])

        test_file = os.path.join(mock_create_labbooks[1], 'default', 'default', 'labbooks',
                                 'labbook1', 'code', 'test.txt')
        with open(test_file, 'wt') as tf:
            tf.write("a test file...")

        # Add a favorite in code
        query = """
        mutation addFavorite {
          addFavorite(
            input: {
              owner: "default",
              labbookName: "labbook1",
              subdir: "code",
              key: "test.txt",
              description: "my test favorite"
            }) {
              newFavoriteEdge{
                node{
                   id
                   index
                   key
                   description
                   isDir
                   }
              }
            }
        }
        """
        snapshot.assert_match(client.execute(query))

        # Verify the favorite is there
        fav_query = """
                           {
                             labbook(name: "labbook1", owner: "default") {
                               name
                               favorites(subdir: "code") {
                                   edges {
                                       node {
                                           id
                                           index
                                           key
                                           description
                                           isDir
                                       }
                                   }
                               }
                             }
                           }
                           """
        snapshot.assert_match(client.execute(fav_query))

        # Delete a favorite in code
        query = """
        mutation deleteFavorite {
          removeFavorite(
            input: {
              owner: "default",
              labbookName: "labbook1",
              subdir: "code",
              index: 0
            }) {
              success
            }
        }
        """
        snapshot.assert_match(client.execute(query))

        # Make sure favorite is gone now
        snapshot.assert_match(client.execute(fav_query))


