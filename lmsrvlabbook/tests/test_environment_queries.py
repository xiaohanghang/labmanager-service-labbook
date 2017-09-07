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
import multiprocessing
import threading
import time
import pytest
import tempfile
import os
import uuid
import shutil
from snapshottest import snapshot

from graphene.test import Client
import graphene
from mock import patch
import rq

from lmcommon.dispatcher import Dispatcher, jobs
from lmcommon.labbook import LabBook
from lmcommon.configuration import Configuration
from lmcommon.environment import ComponentManager

from lmsrvlabbook.tests.fixtures import schema_and_env_index
from lmsrvlabbook.api.query import LabbookQuery
from lmsrvlabbook.api.mutation import LabbookMutations


# Create ObjectType clases, since the EnvironmentQueries and EnvironmentMutations
# are abstract (allowing multiple inheritance)
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


class TestEnvironmentServiceQueries(object):
    def test_get_environment_status(self, mock_config_file, snapshot):
        """Test getting the a LabBook's environment status"""
        # Create labbooks
        lb = LabBook(mock_config_file[0])
        lb.new(owner={"username": "default"}, name="labbook10", description="my first labbook10000")

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            # Make and validate request
            client = Client(mock_config_file[2])

            query = """
            {
              labbook(owner: "default", name: "labbook10") {
                  environment {
                    containerStatus
                    imageStatus
                  }
              }
            }
            """
            snapshot.assert_match(client.execute(query))

    def test_get_base_image(self, schema_and_env_index, snapshot):
        """Test getting the a LabBook's base image"""
        # Create labbook
        lb = LabBook(schema_and_env_index[0])
        lb.new(owner={"username": "default"}, name="labbook1", description="my first labbook10000")

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: schema_and_env_index[0]):
            # Make and validate request
            client = Client(schema_and_env_index[2])

            query = """
                    {
                      labbook(owner: "default", name: "labbook1") {
                        environment {
                          baseImage {
                            id
                            component {
                              repository
                              namespace
                              name
                              componentClass
                              version
                            }
                            info {
                              name
                              humanName
                              versionMajor
                              versionMinor
                            }
                            author {
                              organization
                            }
                            availablePackageManagers
                            server
                            tag
                          }
                        }
                      }
                    }
            """
            # should be null
            snapshot.assert_match(client.execute(query))

            # Add a base image
            cm = ComponentManager(lb)
            cm.add_component("base_image",
                             "gig-dev_environment-components",
                             "gigantum",
                             "ubuntu1604-python3",
                             "0.4")

            # Test again
            snapshot.assert_match(client.execute(query))

    def test_get_dev_env(self, schema_and_env_index, snapshot):
        """Test getting the a LabBook's development environment"""
        # Create labbook
        lb = LabBook(schema_and_env_index[0])
        lb.new(owner={"username": "default"}, name="labbook2", description="my first labbook10000")

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: schema_and_env_index[0]):
            # Make and validate request
            client = Client(schema_and_env_index[2])

            query = """
                    {
                      labbook(owner: "default", name: "labbook2") {
                        environment {
                          devEnvs(first: 1) {
                            edges {
                              node {
                                id
                                component {
                                  repository
                                  namespace
                                  name
                                  componentClass
                                  version
                                }
                                info {
                                  name
                                  humanName
                                  versionMajor
                                  versionMinor
                                }
                                author {
                                  organization
                                }
                                osBaseClass
                                developmentEnvironmentClass
                                installCommands
                                exposedTcpPorts
                                execCommands
                              }
                              cursor
                            }
                            pageInfo {
                              hasNextPage
                              hasPreviousPage
                            }
                          }   
                        }
                      }
                    }
            """
            # should be null
            snapshot.assert_match(client.execute(query))

            # Add a base image
            cm = ComponentManager(lb)
            cm.add_component("dev_env",
                             "gig-dev_environment-components",
                             "gigantum",
                             "jupyter-ubuntu",
                             "0.1")

            # Test again
            snapshot.assert_match(client.execute(query))

    def test_get_custom(self, schema_and_env_index, snapshot):
        """Test getting the a LabBook's custom dependencies"""
        # Create labbook
        lb = LabBook(schema_and_env_index[0])
        lb.new(owner={"username": "default"}, name="labbook3", description="my first labbook10000")

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: schema_and_env_index[0]):
            # Make and validate request
            client = Client(schema_and_env_index[2])

            query = """
                        {
                          labbook(owner: "default", name: "labbook3") {
                            environment {
                             customDependencies(first: 1) {
                                edges {
                                  node {
                                    id
                                    component {
                                      repository
                                      namespace
                                      name
                                      componentClass
                                      version
                                    }
                                    info {
                                      name
                                      humanName
                                      versionMajor
                                      versionMinor
                                    }
                                    author {
                                      organization
                                    }
                                    osBaseClass
                                    docker
                                  }
                                  cursor
                                }
                                pageInfo {
                                  hasNextPage
                                }
                              }
                            }
                          }
                        }            
                        """
            # should be null
            snapshot.assert_match(client.execute(query))

            # Add a base image
            cm = ComponentManager(lb)
            cm.add_component("custom",
                             "gig-dev_environment-components",
                             "gigantum",
                             "ubuntu-python3-pillow",
                             "0.3")

            # Test again
            snapshot.assert_match(client.execute(query))

    def test_get_package_manager(self, schema_and_env_index, snapshot):
        """Test getting the a LabBook's package manager dependencies"""
        # Create labbook
        lb = LabBook(schema_and_env_index[0])
        lb.new(owner={"username": "default"}, name="labbook4", description="my first labbook10000")

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: schema_and_env_index[0]):
            # Make and validate request
            client = Client(schema_and_env_index[2])

            query = """
                        {
                          labbook(owner: "default", name: "labbook4") {
                            environment {
                             packageManagerDependencies(first: 1) {
                                edges {
                                  node {
                                    id
                                    packageName
                                    packageManager
                                    packageVersion
                                  }
                                  cursor
                                }
                                pageInfo {
                                  hasNextPage
                                }
                              }
                            }
                          }
                        }
                        """
            # should be null
            snapshot.assert_match(client.execute(query))

            # Add a base image
            cm = ComponentManager(lb)
            cm.add_package("apt-get", "docker")
            cm.add_package("apt-get", "lxml")
            cm.add_package("pip3", "requests")
            cm.add_package("pip3", "numpy", "1.12")

            # Test again
            snapshot.assert_match(client.execute(query))

            query = """
                       {
                         labbook(owner: "default", name: "labbook4") {
                           environment {
                            packageManagerDependencies(first: 4, after: "MA==") {
                               edges {
                                 node {
                                   id
                                   packageName
                                   packageManager
                                   packageVersion
                                 }
                                 cursor
                               }
                               pageInfo {
                                 hasNextPage
                               }
                             }
                           }
                         }
                       }
                       """
            # should be null
            snapshot.assert_match(client.execute(query))
