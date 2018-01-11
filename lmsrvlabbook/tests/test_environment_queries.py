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
from graphene.test import Client
import graphene
from mock import patch

from lmcommon.labbook import LabBook
from lmcommon.configuration import Configuration
from lmcommon.environment import ComponentManager

from lmsrvlabbook.tests.fixtures import fixture_working_dir_env_repo_scoped, fixture_working_dir


class TestEnvironmentServiceQueries(object):
    def test_get_environment_status(self, fixture_working_dir, snapshot):
        """Test getting the a LabBook's environment status"""
        # Create labbooks
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook10", description="my first labbook10000")

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
        snapshot.assert_match(fixture_working_dir[2].execute(query))

    def test_get_base_image(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the a LabBook's base image"""
        # Create labbook
        lb = LabBook(fixture_working_dir_env_repo_scoped[0])
        lb.new(owner={"username": "default"}, name="labbook1", description="my first labbook10000")

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
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(query))

        # Add a base image
        cm = ComponentManager(lb)
        cm.add_component("base_image",
                         "gig-dev_environment-components",
                         "gigantum",
                         "ubuntu1604-python3",
                         "0.4")

        # Test again
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(query))

    def test_get_dev_env(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the a LabBook's development environment"""
        # Create labbook
        lb = LabBook(fixture_working_dir_env_repo_scoped[0])
        lb.new(owner={"username": "default"}, name="labbook2", description="my first labbook10000")

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_env_repo_scoped[0]):
            # Make and validate request
            client = Client(fixture_working_dir_env_repo_scoped[2])

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

    def test_get_custom(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the a LabBook's custom dependencies"""
        # Create labbook
        lb = LabBook(fixture_working_dir_env_repo_scoped[0])
        lb.new(owner={"username": "default"}, name="labbook3", description="my first labbook10000")

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
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(query))

        # Add a base image
        cm = ComponentManager(lb)
        cm.add_component("custom",
                         "gig-dev_environment-components",
                         "gigantum",
                         "ubuntu-python3-pillow",
                         "0.3")

        # Test again
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(query))

    def test_get_package_manager(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the a LabBook's package manager dependencies"""
        # Create labbook
        lb = LabBook(fixture_working_dir_env_repo_scoped[0])
        lb.new(owner={"username": "default"}, name="labbook4", description="my first labbook10000")

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
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(query))

        # Add a base image
        cm = ComponentManager(lb)
        cm.add_package("apt-get", "docker")
        cm.add_package("apt-get", "lxml")
        cm.add_package("pip3", "requests")
        cm.add_package("pip3", "numpy", "1.12")

        # Test again
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(query))

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
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(query))
