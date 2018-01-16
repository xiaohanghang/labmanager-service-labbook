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
import pprint

class TestEnvironmentBaseImageQueries(object):
    def test_get_available_base_images(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the available base images"""
        query = """
                {
                  availableBases(first: 3) {
                    edges {
                      node {
                        id
                        repository
                        componentId
                        revision
                        name
                        description
                        readme
                        tags
                        icon
                        osClass
                        osRelease
                        license
                        url
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

        result = fixture_working_dir_env_repo_scoped[2].execute(query)
        assert 'errors' not in result
        snapshot.assert_match(result)

    def test_get_available_base_images_pagination(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the available base images"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_env_repo_scoped[0]):
            # Make and validate request
            client = fixture_working_dir_env_repo_scoped[2]

            query = """
                    {
                      availableBases(first: 1){
                        edges{
                          node{
                            id
                            name
                          }
                          cursor
                        }
                        pageInfo{
                          hasNextPage
                        }
                      }
                    }
            """

            result_1 = client.execute(query)
            pprint.pprint(result_1)
            assert 'errors' not in result_1
            snapshot.assert_match(result_1)

            query = """
                    {
                      availableBases(first: 2, after: "MA=="){
                        edges{
                          node{
                            id
                            name
                          }
                          cursor
                        }
                        pageInfo{
                          hasNextPage
                        }
                      }
                    }
            """
            result_2 = client.execute(query)
            pprint.pprint(result_2)
            assert 'errors' not in result_2
            snapshot.assert_match(client.execute(query))

    def test_get_available_base_images_pagination_reverse(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the available base images using pagination from the end"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_env_repo_scoped[0]):
            # Make and validate request
            client = fixture_working_dir_env_repo_scoped[2]

            query = """
                    {
                      availableBases(last: 1){
                        edges{
                          node{
                            id
                            name
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
            result_1 = client.execute(query)
            pprint.pprint(result_1)
            assert 'errors' not in result_1
            snapshot.assert_match(result_1)

            query = """
                    {
                      availableBases(last: 2, before: "MQ=="){
                        edges{
                          node{
                            id
                            name
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
            result_2 = client.execute(query)
            assert 'errors' not in result_2
            pprint.pprint(result_2)
            snapshot.assert_match(result_2)

    def test_get_base_image_by_node(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the available base images"""
        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_env_repo_scoped[0]):
            # Make and validate reques
            client = fixture_working_dir_env_repo_scoped[2]

            query = """
                        {
                          node(id: "QmFzZUNvbXBvbmVudDpnaWctZGV2X2NvbXBvbmVudHMyJnF1aWNrc3RhcnQtanVweXRlcmxhYiYx") {
                            ... on BaseComponent {
                                id
                                repository
                                componentId
                                revision
                                name
                                description
                                readme
                                tags
                                icon
                                osClass
                                osRelease
                                license
                                url
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
            """
            result = client.execute(query)
            assert 'errors' not in result
            snapshot.assert_match(result)