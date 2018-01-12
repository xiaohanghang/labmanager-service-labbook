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


class TestEnvironmentBaseImageQueries(object):
    def test_get_available_base_images(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the available base images"""
        query = """
                {
                  availableBases(first: 3) {
                    edges {
                      node {
                        id
                        component_id
                        name
                        description
                        readme
                        version
                        tags
                        icon
                        osClass
                        osRelease
                        license
                        url
                        maintainers
                        languages
                        developmentTools
                        dockerImageServer
                        dockerImageNamespace
                        dockerImageRepository
                        dockerImageTag
                        packageManagers
                      }
                    }
                  }
                }
        """

        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(query))

    def test_get_available_base_images_pagination(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the available base images"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_env_repo_scoped[0]):
            # Make and validate request
            client = Client(fixture_working_dir_env_repo_scoped[2])

            query = """
                    {
                      availableBaseImages(first: 1){
                        edges{
                          node{
                            id
                            component{
                              repository
                              namespace
                              name
                              componentClass
                              version
                            }
                            info{                              
                              name
                              humanName
                              versionMajor
                              versionMinor
                            }
                            server
                            repository
                            namespace
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
                            server
                            namespace
                            repository
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

    def test_get_available_base_images_pagination_reverse(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the available base images using pagination from the end"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_env_repo_scoped[0]):
            # Make and validate request
            client = Client(fixture_working_dir_env_repo_scoped[2])

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
                            server
                            namespace
                            repository
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
                            server
                            namespace
                            repository
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

    def test_get_base_image_by_node(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the available base images"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_env_repo_scoped[0]):
            # Make and validate request
            client = Client(fixture_working_dir_env_repo_scoped[2])

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


    # def test_get_available_base_image_versions(self, fixture_working_dir_env_repo_scoped, snapshot):
    #     """Test getting the available base image versions for a given component"""
    #     # Mock the configuration class it it returns the same mocked config file
    #     with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_env_repo_scoped[0]):
    #         # Make and validate request
    #         client = Client(fixture_working_dir_env_repo_scoped[2])
    #
    #         query = """
    #                 {
    #                   availableBaseImageVersions(first: 3, repository: "gig-dev_environment-components",
    #                    namespace: "gigantum",
    #                    component: "ubuntu1604-python3"){
    #                     edges{
    #                       node{
    #                         id
    #                         info{
    #                           name
    #                           humanName
    #                           versionMajor
    #                           versionMinor
    #                         }
    #                       }
    #                     }
    #                   }
    #                 }
    #         """
    #         snapshot.assert_match(client.execute(query))
    #
    # def test_get_available_base_image_versions_pagination(self, fixture_working_dir_env_repo_scoped, snapshot):
    #     """Test getting the available base image versions for a given component with pagination"""
    #     # Mock the configuration class it it returns the same mocked config file
    #     with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_env_repo_scoped[0]):
    #         # Make and validate request
    #         client = Client(fixture_working_dir_env_repo_scoped[2])
    #
    #         query = """
    #                 {
    #                   availableBaseImageVersions(first: 3,
    #                      repository: "gig-dev_environment-components",
    #                      namespace: "gigantum", component: "ubuntu1604-python3"){
    #                     edges{
    #                       node{
    #                         id
    #                         info{
    #                           name
    #                           humanName
    #                           versionMajor
    #                           versionMinor
    #                         }
    #                       }
    #                       cursor
    #                     }
    #                     pageInfo{
    #                       hasNextPage
    #                       hasPreviousPage
    #                     }
    #                   }
    #                 }
    #         """
    #         snapshot.assert_match(client.execute(query))
    #
    #         query = """
    #                 {
    #                   availableBaseImageVersions(first: 3, after: "Mg==",
    #                      repository: "gig-dev_environment-components",
    #                      namespace: "gigantum", component: "ubuntu1604-python3"){
    #                     edges{
    #                       node{
    #                         id
    #                         info{
    #                           name
    #                           humanName
    #                           versionMajor
    #                           versionMinor
    #                         }
    #                       }
    #                       cursor
    #                     }
    #                     pageInfo{
    #                       hasNextPage
    #                       hasPreviousPage
    #                     }
    #                   }
    #                 }
    #         """
    #         snapshot.assert_match(client.execute(query))
    #
    # def test_get_available_base_image_versions_pagination_reverse(self, fixture_working_dir_env_repo_scoped, snapshot):
    #     """Test getting the available base image versions for a given component with pagination"""
    #     # Mock the configuration class it it returns the same mocked config file
    #     with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_env_repo_scoped[0]):
    #         # Make and validate request
    #         client = Client(fixture_working_dir_env_repo_scoped[2])
    #
    #         query = """
    #                 {
    #                   availableBaseImageVersions(last: 3,
    #                      repository: "gig-dev_environment-components",
    #                      namespace: "gigantum", component: "ubuntu1604-python3"){
    #                     edges{
    #                       node{
    #                         id
    #                         info{
    #                           name
    #                           humanName
    #                           versionMajor
    #                           versionMinor
    #                         }
    #                       }
    #                       cursor
    #                     }
    #                     pageInfo{
    #                       hasNextPage
    #                       hasPreviousPage
    #                     }
    #                   }
    #                 }
    #         """
    #         snapshot.assert_match(client.execute(query))
    #
    #         query = """
    #                 {
    #                   availableBaseImageVersions(last: 3, before: "MQ==",
    #                      repository: "gig-dev_environment-components",
    #                      namespace: "gigantum", component: "ubuntu1604-python3"){
    #                     edges{
    #                       node{
    #                         id
    #                         info{
    #                           name
    #                           humanName
    #                           versionMajor
    #                           versionMinor
    #                         }
    #                       }
    #                       cursor
    #                     }
    #                     pageInfo{
    #                       hasNextPage
    #                       hasPreviousPage
    #                     }
    #                   }
    #                 }
    #         """
    #         snapshot.assert_match(client.execute(query))


