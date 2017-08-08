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

from lmcommon.environment import RepositoryManager
from lmcommon.configuration import Configuration

from lmsrvlabbook.api.query import LabbookQuery
from lmsrvlabbook.api.mutation import LabbookMutations


# Create ObjectType clases, since the EnvironmentQueries and EnvironmentMutations
# are abstract (allowing multiple inheritance)
class Query(LabbookQuery, graphene.ObjectType):
    pass


class Mutation(LabbookMutations, graphene.ObjectType):
    pass


@pytest.fixture(scope="module")
def mock_config_file():
    """A pytest fixture that creates a temporary directory and a config file to match. Deletes directory after test"""
    # Create a temporary working directory
    temp_dir = os.path.join(tempfile.tempdir, uuid.uuid4().hex)
    os.makedirs(temp_dir)

    with tempfile.NamedTemporaryFile(mode="wt") as fp:
        # Write a temporary config file
        fp.write("""core:
  team_mode: false 
  
environment:
  repo_url:
    - "https://github.com/gig-dev/environment-components.git"
    
git:
  backend: 'filesystem'
  working_directory: '{}'""".format(temp_dir))
        fp.seek(0)

        # Create test client
        schema = graphene.Schema(query=Query,
                                 mutation=Mutation)

        # get environment data and index
        erm = RepositoryManager(fp.name)
        erm.update_repositories()
        erm.index_repositories()

        yield fp.name, temp_dir, schema  # name of the config file, temporary working directory, the schema

    # Remove the temp_dir
    shutil.rmtree(temp_dir)


class TestEnvironmentBaseImageQueries(object):
    def test_get_available_base_images(self, mock_config_file, snapshot):
        """Test getting the available base images"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            # Make and validate request
            client = Client(mock_config_file[2])

            query = """
                    {
                      availableBaseImages(first: 3){
                        edges{
                          node{
                            id
                            info{                              
                              name
                              humanName
                              versionMajor
                              versionMinor
                            }
                            author{
                              organization
                            }
                            availablePackageManagers
                            server
                            namespace
                            repo
                            tag
                          }
                        }
                      }
                    }
            """
            snapshot.assert_match(client.execute(query))

    def test_get_available_base_images_pagination(self, mock_config_file, snapshot):
        """Test getting the available base images"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            # Make and validate request
            client = Client(mock_config_file[2])

            query = """
                    {
                      availableBaseImages(first: 1){
                        edges{
                          node{
                            id
                            info{                              
                              name
                              humanName
                              versionMajor
                              versionMinor
                            }
                            namespace
                            repo
                            tag
                          }
                          cursor
                        }
                        pageInfo{
                          hasNextPage
                        }
                      }
                    }
            """
            snapshot.assert_match(client.execute(query))

            query = """
                    {
                      availableBaseImages(first: 2, after: "MA=="){
                        edges{
                          node{
                            info{
                              id
                              name
                              humanName
                              versionMajor
                              versionMinor
                            }
                            namespace
                            repo
                            tag
                          }
                          cursor
                        }
                        pageInfo{
                          hasNextPage
                        }
                      }
                    }
            """
            snapshot.assert_match(client.execute(query))

    def test_get_available_base_images_pagination_reverse(self, mock_config_file, snapshot):
        """Test getting the available base images using pagination from the end"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            # Make and validate request
            client = Client(mock_config_file[2])

            query = """
                    {
                      availableBaseImages(last: 1){
                        edges{
                          node{
                            id
                            info{                              
                              name
                              humanName
                              versionMajor
                              versionMinor
                            }
                            namespace
                            repo
                            tag
                          }
                          cursor
                        }
                        pageInfo{
                          hasNextPage
                          hasPreviousPage
                        }
                      }
                    }
            """
            snapshot.assert_match(client.execute(query))

            query = """
                    {
                      availableBaseImages(last: 2, before: "MQ=="){
                        edges{
                          node{
                            info{
                              id
                              name
                              humanName
                              versionMajor
                              versionMinor
                            }
                            namespace
                            repo
                            tag
                          }
                          cursor
                        }
                        pageInfo{
                          hasNextPage
                          hasPreviousPage
                        }
                      }
                    }
            """
            snapshot.assert_match(client.execute(query))

    def test_get_base_image_by_node(self, mock_config_file, snapshot):
        """Test getting the available base images"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            # Make and validate request
            client = Client(mock_config_file[2])

            query = """
                        {
                          node(id: "QmFzZUltYWdlOmJhc2VfaW1hZ2UmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dTE2MDQtcHl0aG9uMyYwLjQ=") {
                            ... on BaseImage {
                              info {
                                name
                                humanName
                                versionMajor
                                versionMinor
                              }
                            }
                          }
                        }
            """
            snapshot.assert_match(client.execute(query))

    def test_get_available_base_image_versions(self, mock_config_file, snapshot):
        """Test getting the available base image versions for a given component"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            # Make and validate request
            client = Client(mock_config_file[2])

            query = """
                    {
                      availableBaseImageVersions(first: 3, repository: "gig-dev_environment-components",
                       namespace: "gigantum",
                       component: "ubuntu1604-python3"){
                        edges{
                          node{
                            id
                            info{          
                              name
                              humanName
                              versionMajor
                              versionMinor
                            }
                          }
                        }
                      }
                    }
            """
            snapshot.assert_match(client.execute(query))

    def test_get_available_base_image_versions_pagination(self, mock_config_file, snapshot):
        """Test getting the available base image versions for a given component with pagination"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            # Make and validate request
            client = Client(mock_config_file[2])

            query = """
                    {
                      availableBaseImageVersions(first: 3,
                         repository: "gig-dev_environment-components",
                         namespace: "gigantum", component: "ubuntu1604-python3"){
                        edges{
                          node{
                            id
                            info{          
                              name
                              humanName
                              versionMajor
                              versionMinor
                            }
                          }
                          cursor
                        }
                        pageInfo{
                          hasNextPage
                          hasPreviousPage
                        }
                      }
                    }
            """
            snapshot.assert_match(client.execute(query))

            query = """
                    {
                      availableBaseImageVersions(first: 3, after: "Mg==", 
                         repository: "gig-dev_environment-components",
                         namespace: "gigantum", component: "ubuntu1604-python3"){
                        edges{
                          node{
                            id
                            info{          
                              name
                              humanName
                              versionMajor
                              versionMinor
                            }
                          }
                          cursor
                        }
                        pageInfo{
                          hasNextPage
                          hasPreviousPage
                        }
                      }
                    }
            """
            snapshot.assert_match(client.execute(query))

    def test_get_available_base_image_versions_pagination_reverse(self, mock_config_file, snapshot):
        """Test getting the available base image versions for a given component with pagination"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            # Make and validate request
            client = Client(mock_config_file[2])

            query = """
                    {
                      availableBaseImageVersions(last: 3,
                         repository: "gig-dev_environment-components",
                         namespace: "gigantum", component: "ubuntu1604-python3"){
                        edges{
                          node{
                            id
                            info{          
                              name
                              humanName
                              versionMajor
                              versionMinor
                            }
                          }
                          cursor
                        }
                        pageInfo{
                          hasNextPage
                          hasPreviousPage
                        }
                      }
                    }
            """
            snapshot.assert_match(client.execute(query))

            query = """
                    {
                      availableBaseImageVersions(last: 3, before: "MQ==", 
                         repository: "gig-dev_environment-components",
                         namespace: "gigantum", component: "ubuntu1604-python3"){
                        edges{
                          node{
                            id
                            info{          
                              name
                              humanName
                              versionMajor
                              versionMinor
                            }
                          }
                          cursor
                        }
                        pageInfo{
                          hasNextPage
                          hasPreviousPage
                        }
                      }
                    }
            """
            snapshot.assert_match(client.execute(query))


