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
from snapshottest import snapshot
from lmsrvlabbook.tests.fixtures import fixture_working_dir_env_repo_scoped
from graphene.test import Client
from mock import patch

from lmcommon.configuration import Configuration


class TestEnvironmentDevEnvQueries(object):
    def test_get_available_dev_envs(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the available development environments"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_env_repo_scoped[0]):
            # Make and validate request
            client = Client(fixture_working_dir_env_repo_scoped[2])

            query = """
                    {
                      availableDevEnvs(first: 3) {
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
                        }
                      }
                    }

            """
            snapshot.assert_match(client.execute(query))

    def test_get_available_dev_envs_pagination(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the available dev envs with pagination"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_env_repo_scoped[0]):
            # Make and validate request
            client = Client(fixture_working_dir_env_repo_scoped[2])

            query = """
                   {
                  availableDevEnvs(first: 1) {
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
                    }
                  }
                }
            """
            snapshot.assert_match(client.execute(query))

            query = """
                    {
                      availableDevEnvs(first: 3, after: "MA==") {
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
                        }
                        pageInfo {
                          hasNextPage
                        }
                      }
                    }
            """
            snapshot.assert_match(client.execute(query))

    def test_get_available_dev_envs_pagination_reverse(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the available development environments using pagination from the end"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_env_repo_scoped[0]):
            # Make and validate request
            client = Client(fixture_working_dir_env_repo_scoped[2])

            query = """
                    {
                      availableDevEnvs(last: 1) {
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
                        }
                        pageInfo {
                          hasPreviousPage
                          hasNextPage
                        }
                      }
                    }            
                    """
            snapshot.assert_match(client.execute(query))

            query = """
                    {
                      availableDevEnvs(last: 3, before: "Mg==") {
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
                        }
                        pageInfo {
                          hasPreviousPage
                          hasNextPage
                        }
                      }
                    }
                    """
            snapshot.assert_match(client.execute(query))

    def test_get_dev_env_by_node(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting a dev env by node ID"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_env_repo_scoped[0]):
            # Make and validate request
            client = Client(fixture_working_dir_env_repo_scoped[2])

            query = """
                        {
                          node(id: "RGV2RW52OmRldl9lbnYmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtLWRldiZqdXB5dGVyLXVidW50dSYwLjE=") {
                            ... on DevEnv {
                              info {
                                name
                                humanName
                                versionMajor
                                versionMinor
                              }
                              component{
                                repository
                                namespace
                                name
                                componentClass
                                version
                              }
                            }
                          }
                        }
            """
            snapshot.assert_match(client.execute(query))

    def test_get_available_dev_env_versions(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the available versions for a given component"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_env_repo_scoped[0]):
            # Make and validate request
            client = Client(fixture_working_dir_env_repo_scoped[2])

            query = """
                        {
                          availableDevEnvVersions(first: 3, 
                            repository: "gig-dev_environment-components",
                            namespace: "gigantum", component: "jupyter-ubuntu") {
                            edges {
                              node {
                                id
                                info {
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

    def test_get_available_dev_env_versions_pagination(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the available versions for a given component with pagination"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_env_repo_scoped[0]):
            # Make and validate request
            client = Client(fixture_working_dir_env_repo_scoped[2])

            query = """
                       {
                          availableDevEnvVersions(first: 1, 
                            repository: "gig-dev_environment-components",
                            namespace: "gigantum", component: "jupyter-ubuntu") {
                            edges {
                              node {
                                id
                                info {
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
                          availableDevEnvVersions(first: 1, after: "MA==" 
                            repository: "gig-dev_environment-components",
                            namespace: "gigantum", component: "jupyter-ubuntu") {
                            edges {
                              node {
                                id
                                info {
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

    def test_get_available_dev_env_versions_pagination_reverse(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the available versions for a given component with pagination in reverse"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_env_repo_scoped[0]):
            # Make and validate request
            client = Client(fixture_working_dir_env_repo_scoped[2])

            query = """
                       {
                          availableDevEnvVersions(last: 1, 
                            repository: "gig-dev_environment-components",
                            namespace: "gigantum", component: "jupyter-ubuntu") {
                            edges {
                              node {
                                id
                                info {
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
                          availableDevEnvVersions(last: 3, before: "MQ==" 
                            repository: "gig-dev_environment-components",
                            namespace: "gigantum", component: "jupyter-ubuntu") {
                            edges {
                              node {
                                id
                                info {
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
