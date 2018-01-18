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


class TestEnvironmentCustomDependencyQueries(object):
    def test_get_available_custom_deps(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the available custom dependencies"""
        query = """
               {
                  availableCustomDependencies {
                    edges {
                      node {
                        id
                        componentId
                        repository
                        revision
                        name
                        description                        
                        tags
                        license
                        url
                        requiredPackageManagers
                        dockerSnippet
                      }
                    }
                  }
                }
        """
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(query))

    def test_get_available_custom_deps_pagination(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the available custom dependencies"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_env_repo_scoped[0]):
            # Make and validate request
            client = Client(fixture_working_dir_env_repo_scoped[2])

            query = """
                    {
                      availableCustomDependencies(first: 1) {
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
                          hasPreviousPage
                        }
                      }
                    }

            """
            snapshot.assert_match(client.execute(query))

            query = """
 {
                      availableCustomDependencies(first: 2, after: "MA==") {
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
                          hasPreviousPage
                        }
                      }
                    }
            """
            snapshot.assert_match(client.execute(query))

    def test_get_available_custom_deps_pagination_reverse(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the available custom dependencies using pagination from the end"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_env_repo_scoped[0]):
            # Make and validate request
            client = Client(fixture_working_dir_env_repo_scoped[2])

            query = """
                    {
                      availableCustomDependencies(last: 1) {
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
                          hasPreviousPage
                        }
                      }
                    }

                    """
            snapshot.assert_match(client.execute(query))

            query = """
                    {
                      availableCustomDependencies(last: 2, before: "MQ==") {
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
                          hasPreviousPage
                        }
                      }
                    }

                   """
            snapshot.assert_match(client.execute(query))

    def test_get_custom_deps_by_node(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the available custom dependency by node ID"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_env_repo_scoped[0]):
            # Make and validate request
            client = Client(fixture_working_dir_env_repo_scoped[2])

            query = """
                        {
                          node(id: "Q3VzdG9tRGVwZW5kZW5jeTpjdXN0b20mZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dS1weXRob24zLXBpbGxvdyYwLjE=") {
                            ... on CustomDependency {
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

    # def test_get_available_custom_deps_versions(self, fixture_working_dir_env_repo_scoped, snapshot):
    #     """Test getting the available versions for a given component"""
    #     # Mock the configuration class it it returns the same mocked config file
    #     with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_env_repo_scoped[0]):
    #         # Make and validate request
    #         client = Client(fixture_working_dir_env_repo_scoped[2])
    #
    #         query = """
    #                     {
    #                       availableCustomDependenciesVersions(repository: "gig-dev_environment-components",
    #                                                 namespace: "gigantum",component: "ubuntu-python3-pillow") {
    #                         edges {
    #                           node {
    #                             id
    #                             component {
    #                               repository
    #                               namespace
    #                               name
    #                               componentClass
    #                               version
    #                             }
    #                             info {
    #                               name
    #                               humanName
    #                               versionMajor
    #                               versionMinor
    #                             }
    #                           }
    #                           cursor
    #                         }
    #                         pageInfo {
    #                           hasNextPage
    #                           hasPreviousPage
    #                         }
    #                       }
    #                     }
    #         """
    #         snapshot.assert_match(client.execute(query))
    #
    # def test_get_available_custom_deps_versions_pagination(self, fixture_working_dir_env_repo_scoped, snapshot):
    #     """Test getting the available versions for a given component with pagination"""
    #     # Mock the configuration class it it returns the same mocked config file
    #     with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_env_repo_scoped[0]):
    #         # Make and validate request
    #         client = Client(fixture_working_dir_env_repo_scoped[2])
    #
    #         query = """
    #                     {
    #                       availableCustomDependenciesVersions(first: 2, repository: "gig-dev_environment-components",
    #                                                 namespace: "gigantum",component: "ubuntu-python3-pillow") {
    #                         edges {
    #                           node {
    #                             id
    #                             component {
    #                               repository
    #                               namespace
    #                               name
    #                               componentClass
    #                               version
    #                             }
    #                             info {
    #                               name
    #                               humanName
    #                               versionMajor
    #                               versionMinor
    #                             }
    #                           }
    #                           cursor
    #                         }
    #                         pageInfo {
    #                           hasNextPage
    #                           hasPreviousPage
    #                         }
    #                       }
    #                     }
    #         """
    #         snapshot.assert_match(client.execute(query))
    #
    #         query = """
    #                     {
    #                       availableCustomDependenciesVersions(first: 2, after: "MQ==",
    #                                                 repository: "gig-dev_environment-components",
    #                                                 namespace: "gigantum",component: "ubuntu-python3-pillow") {
    #                         edges {
    #                           node {
    #                             id
    #                             component {
    #                               repository
    #                               namespace
    #                               name
    #                               componentClass
    #                               version
    #                             }
    #                             info {
    #                               name
    #                               humanName
    #                               versionMajor
    #                               versionMinor
    #                             }
    #                           }
    #                           cursor
    #                         }
    #                         pageInfo {
    #                           hasNextPage
    #                           hasPreviousPage
    #                         }
    #                       }
    #                     }
    #         """
    #         snapshot.assert_match(client.execute(query))
    #
    # def test_get_available_custom_deps_versions_pagination_reverse(self, fixture_working_dir_env_repo_scoped, snapshot):
    #     """Test getting the available versions for a given component with pagination in reverse"""
    #     # Mock the configuration class it it returns the same mocked config file
    #     with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_env_repo_scoped[0]):
    #         # Make and validate request
    #         client = Client(fixture_working_dir_env_repo_scoped[2])
    #
    #         query = """
    #                     {
    #                       availableCustomDependenciesVersions(last: 2, repository: "gig-dev_environment-components",
    #                                                 namespace: "gigantum",component: "ubuntu-python3-pillow") {
    #                         edges {
    #                           node {
    #                             id
    #                             component {
    #                               repository
    #                               namespace
    #                               name
    #                               componentClass
    #                               version
    #                             }
    #                             info {
    #                               name
    #                               humanName
    #                               versionMajor
    #                               versionMinor
    #                             }
    #                           }
    #                           cursor
    #                         }
    #                         pageInfo {
    #                           hasNextPage
    #                           hasPreviousPage
    #                         }
    #                       }
    #                     }
    #         """
    #         snapshot.assert_match(client.execute(query))
    #
    #         query = """
    #                     {
    #                       availableCustomDependenciesVersions(last: 2, before: "MQ==",
    #                                                 repository: "gig-dev_environment-components",
    #                                                 namespace: "gigantum",component: "ubuntu-python3-pillow") {
    #                         edges {
    #                           node {
    #                             id
    #                             component {
    #                               repository
    #                               namespace
    #                               name
    #                               componentClass
    #                               version
    #                             }
    #                             info {
    #                               name
    #                               humanName
    #                               versionMajor
    #                               versionMinor
    #                             }
    #                           }
    #                           cursor
    #                         }
    #                         pageInfo {
    #                           hasNextPage
    #                           hasPreviousPage
    #                         }
    #                       }
    #                     }
    #         """
    #         snapshot.assert_match(client.execute(query))
