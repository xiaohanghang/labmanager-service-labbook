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

    def test_delete_file(self, mock_create_labbooks):
        with patch.object(Configuration, 'find_default_config', lambda self: mock_create_labbooks[0]):
            client = Client(mock_create_labbooks[2])
            # Note, deleting a file should work with and without a trailing / at the end.
            query = """
            mutation deleteLabbookFile {
              deleteLabbookFile(
                input: {
                  user: "default",
                  owner: "default",
                  labbookName: "labbook1",
                  filePath: "code/",
                  isDirectory: true
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
                self.files = {'uploadChunk': file_handle}

        client = Client(mock_create_labbooks[2])

        # Create file to upload
        test_file = os.path.join(tempfile.gettempdir(), "myfile.bin")
        with open(test_file, 'wb') as tf:
            tf.write(os.urandom(9000000))

        # Get upload params
        chunk_size = 4194000
        file_info = os.stat(test_file)
        file_size = int(file_info.st_size / 1024)
        total_chunks = int(math.ceil(file_info.st_size / chunk_size))

        target_file = os.path.join(mock_create_labbooks[1], 'default', 'default', 'labbooks',
                                   'labbook1', 'code', 'myfile.bin')

        with open(test_file, 'rb') as tf:
            # Check for file to exist (shouldn't yet)
            assert os.path.exists(target_file) is False

            for chunk_index in range(total_chunks):
                # Upload a chunk
                chunk = io.BytesIO()
                chunk.write(tf.read(chunk_size))
                chunk.seek(0)
                file = FileStorage(chunk)

                query = f"""
                            mutation addLabbookFile{{
                              addLabbookFile(input:{{owner:"default", user:"default",
                                                      labbookName: "labbook1",
                                                      filePath: "code/myfile.bin",
                                chunkUploadParams:{{
                                  uploadId: "jfdjfdjdisdjwdoijwlkfjd",
                                  chunkSize: {chunk_size},
                                  totalChunks: {total_chunks},
                                  chunkIndex: {chunk_index},
                                  fileSizeKb: {file_size},
                                  filename: "{os.path.basename(test_file)}"
                                }}
                              }}) {{
                                      newLabbookFileEdge {{
                                        node{{
                                          id
                                          key
                                          isDir
                                          size
                                        }}
                                      }}
                                    }}
                            }}
                            """
                snapshot.assert_match(client.execute(query, context_value=DummyContext(file)))

        # When done uploading, file should exist in the labbook
        assert os.path.exists(target_file) is True
        assert os.path.isfile(target_file) is True

    def test_add_file_errors(self, mock_create_labbooks, snapshot):
        """Test new file error handling"""
        class DummyContext(object):
            def __init__(self, file_handle):
                self.files = {'blah': file_handle}

        client = Client(mock_create_labbooks[2])
        query = f"""
                    mutation addLabbookFile{{
                      addLabbookFile(input:{{owner:"default", user:"default",
                                              labbookName: "labbook1",
                                              filePath: "code/myfile.bin",
                        chunkUploadParams:{{
                          uploadId: "jfdjfdjdisdjwdoijwlkfjd",
                          chunkSize: 100,
                          totalChunks: 2,
                          chunkIndex: 0,
                          fileSizeKb: 200,
                          filename: "myfile.bin"
                        }}
                      }}) {{
                              newLabbookFileEdge {{
                                node{{
                                  id
                                  key
                                  isDir
                                  size
                                }}
                              }}
                            }}
                    }}
                    """
        # Fail because no file
        snapshot.assert_match(client.execute(query, context_value=DummyContext(None)))

        # DMK - commenting out test because check is currently disabled
        # test_file = os.path.join(tempfile.gettempdir(), "myfile.txt")

        # with open(test_file, 'wt') as tf:
        #     tf.write("THIS IS A FILE I MADE!")

        # with open(test_file, 'rb') as tf:
        #     file = FileStorage(tf)
        #     # Fail because filenames don't match
        #     snapshot.assert_match(client.execute(query, context_value=DummyContext(file)))

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

    def test_import_labbook(self, fixture_working_dir, snapshot):
        """Test batch uploading, but not full import"""
        class DummyContext(object):
            def __init__(self, file_handle):
                self.files = {'uploadChunk': file_handle}

        client = Client(fixture_working_dir[2])

        # Create a temporary labbook
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="test-export", description="Tester")

        # Create a largeish file in the dir
        with open(os.path.join(fixture_working_dir[1], 'testfile.bin'), 'wb') as testfile:
            testfile.write(os.urandom(9000000))
        lb.insert_file(testfile.name, 'input')

        # Export labbook
        zip_file = export_labbook_as_zip(lb.root_dir, tempfile.gettempdir())
        lb_dir = lb.root_dir

        # Get upload params
        chunk_size = 4194304
        file_info = os.stat(zip_file)
        file_size = int(file_info.st_size / 1024)
        total_chunks = int(math.ceil(file_info.st_size/chunk_size))

        with open(zip_file, 'rb') as tf:
            for chunk_index in range(total_chunks):
                chunk = io.BytesIO()
                chunk.write(tf.read(chunk_size))
                chunk.seek(0)
                file = FileStorage(chunk)

                query = f"""
                            mutation myMutation{{
                              importLabbook(input:{{owner:"default", user:"default",
                                chunkUploadParams:{{
                                  uploadId: "jfdjfdjdisdjwdoijwlkfjd",
                                  chunkSize: {chunk_size},
                                  totalChunks: {total_chunks},
                                  chunkIndex: {chunk_index},
                                  fileSizeKb: {file_size},
                                  filename: "{os.path.basename(zip_file)}"
                                }}
                              }}) {{
                                importJobKey
                                buildImageJobKey
                              }}
                            }}
                            """
                result = client.execute(query, context_value=DummyContext(file))
                assert "errors" not in result
                if chunk_index < total_chunks - 1:
                    assert result['data']['importLabbook']['importJobKey'] is None
                    assert result['data']['importLabbook']['buildImageJobKey'] is None
                else:
                    assert type(result['data']['importLabbook']['importJobKey']) == str
                    assert type(result['data']['importLabbook']['buildImageJobKey']) == str
                    assert "rq:job:" in result['data']['importLabbook']['importJobKey']
                    assert "rq:job:" in result['data']['importLabbook']['buildImageJobKey']

                    # TODO: Move this test to integration level test where working dir is properly mocked in the rq worker

                    # # Wait up to 10s for import to complete...if fail raise exception
                    # d = Dispatcher()
                    # t_start = datetime.datetime.now()
                    # success = False
                    # while (datetime.datetime.now() - t_start).seconds < 10:
                    #     status = d.query_task(JobKey(result['data']['importLabbook']['importJobKey']))
                    #     if status.status == 'finished':
                    #         success = True
                    #         break
                    #     elif status.status == 'failed':
                    #         break
                    # assert success is True
                    # assert os.path.exists(abs_lb_path) is True

                chunk.close()

    @pytest.mark.skipif(getpass.getuser() == 'circleci', reason="Cannot build images on CircleCI")
    def test_rename_labbook(self, fixture_working_dir, snapshot):
        """Test renaming a labbook"""
        client = Client(fixture_working_dir[2])

        # Create a dummy labbook to make sure directory structure is set up
        lb_dummy = LabBook(fixture_working_dir[0])
        lb_dummy.new(owner={"username": "default"}, name="dummy-lb", description="Tester dummy lb")

        # Unzip test labbook into working directory
        test_zip_file = os.path.join(resource_filename('lmsrvlabbook', 'tests'), 'data', 'test-labbook.zip')
        labbooks_dir = os.path.join(fixture_working_dir[1], 'default', 'default', 'labbooks')
        with ZipFile(test_zip_file) as zf:
            zf.extractall(labbooks_dir)

        original_dir = os.path.join(labbooks_dir, 'test-labbook')
        new_dir = os.path.join(labbooks_dir, 'test-new-name')

        # rename (without the container being previously built)
        query = f"""
                    mutation myMutation{{
                      renameLabbook(input:{{owner:"default", user:"default", 
                      originalLabbookName: "test-labbook",
                      newLabbookName: "test-new-name"}}) {{
                        success                        
                      }}
                    }}
                    """
        snapshot.assert_match(client.execute(query))

        # Wait up to 15 seconds for the container to build successfully after renaming
        query = """
                   {
                     labbook(owner: "default", name: "test-new-name") {
                         environment {
                           imageStatus
                         }
                     }
                   }
                   """
        t_start = datetime.datetime.now()
        success = False
        while (datetime.datetime.now() - t_start).seconds < 15:
            response = client.execute(query)
            if response['data']['labbook']['environment']['imageStatus'] == 'EXISTS':
                success = True
                break

        # Verify everything worked
        assert success is True
        assert os.path.exists(original_dir) is False
        assert os.path.exists(new_dir) is True

        original_dir = new_dir
        new_dir = os.path.join(labbooks_dir, 'test-renamed-again')

        # rename again (this time the container will have been built)
        query = f"""
                    mutation myMutation{{
                      renameLabbook(input:{{owner:"default", user:"default", 
                      originalLabbookName: "test-new-name",
                      newLabbookName: "test-renamed-again"}}) {{
                        success                        
                      }}
                    }}
                    """
        snapshot.assert_match(client.execute(query))

        # Wait up to 15 seconds for the container to build successfully after renaming
        query = """
                   {
                     labbook(owner: "default", name: "test-renamed-again") {
                         environment {
                           imageStatus
                         }
                     }
                   }
                   """
        t_start = datetime.datetime.now()
        success = False
        while (datetime.datetime.now() - t_start).seconds < 15:
            response = client.execute(query)
            if response['data']['labbook']['environment']['imageStatus'] == 'EXISTS':
                success = True
                break

        # Verify everything worked
        assert success is True
        assert os.path.exists(original_dir) is False
        assert os.path.exists(new_dir) is True