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
import yaml
import os

from snapshottest import snapshot

from lmsrvlabbook.tests.fixtures import fixture_working_dir_env_repo_scoped
from lmcommon.labbook import LabBook


class TestAddComponentMutations(object):

    def test_add_package(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test listing labbooks"""
        lb = LabBook(fixture_working_dir_env_repo_scoped[0])

        labbook_dir = lb.new(name="catbook-package-tester", description="LB to test package mutation",
                             owner={"username": "default"})

        # Add a base image
        pkg_query = """
        mutation myPkgMutation {
          addPackageComponent (input: {
            owner: "default",
            labbookName: "catbook-package-tester",
            package: "requests",
            manager: "pip",
            version: "2.18.4"
          }) {
            clientMutationId
            newPackageComponentEdge {
              node{
                id
                schema
                manager
                package
                version
                fromBase
              }
            }
          }
        }
        """
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(pkg_query))

        # Validate the LabBook .gigantum/env/ directory
        assert os.path.exists(os.path.join(labbook_dir, '.gigantum', 'env', 'package_manager')) is True

        assert os.path.exists(os.path.join(labbook_dir, '.gigantum', 'env', 'package_manager', 'pip_requests.yaml'))

        with open(os.path.join(labbook_dir, '.gigantum', 'env', 'package_manager', 'pip_requests.yaml')) as pkg_yaml:
            package_info_dict = yaml.load(pkg_yaml)
            assert package_info_dict['package'] == 'requests'
            assert package_info_dict['manager'] == 'pip'
            assert package_info_dict['version'] == '2.18.4'
            assert package_info_dict['schema'] == 1
            assert package_info_dict['from_base'] is False

    def test_add_package_no_version(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test adding a package but omitting the version"""
        lb = LabBook(fixture_working_dir_env_repo_scoped[0])

        labbook_dir = lb.new(name="catbook-package-no-version", description="LB to test package mutation",
                             owner={"username": "default"})

        # Add a base image
        pkg_query = """
        mutation myPkgMutation {
          addPackageComponent (input: {
            owner: "default",
            labbookName: "catbook-package-no-version",
            package: "requests",
            manager: "pip"
          }) {
            clientMutationId
            newPackageComponentEdge {
              node{
                id
                schema
                manager
                package
                version
                fromBase
              }
            }
          }
        }
        """
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(pkg_query))
        assert os.path.exists(os.path.join(labbook_dir, '.gigantum', 'env', 'package_manager', 'pip_requests.yaml'))

    def test_add_package_bad_version(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test adding a package with an invalid version"""
        lb = LabBook(fixture_working_dir_env_repo_scoped[0])

        labbook_dir = lb.new(name="catbook-package-bad-version", description="LB to test package mutation",
                             owner={"username": "default"})

        # Add a base image
        pkg_query = """
        mutation myPkgMutation {
          addPackageComponent (input: {
            owner: "default",
            labbookName: "catbook-package-bad-version",
            package: "requests",
            manager: "pip",
            version: "100.100.100"
          }) {
            clientMutationId
            newPackageComponentEdge {
              node{
                id
                schema
                manager
                package
                version
                fromBase
              }
            }
          }
        }
        """
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(pkg_query))
        assert not os.path.exists(os.path.join(labbook_dir, '.gigantum', 'env', 'package_manager', 'pip_requests.yaml'))

    def test_add_bad_package(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test adding a bad package"""
        lb = LabBook(fixture_working_dir_env_repo_scoped[0])

        labbook_dir = lb.new(name="catbook-package-bad", description="LB to test package mutation",
                             owner={"username": "default"})

        # Add a base image
        pkg_query = """
        mutation myPkgMutation {
          addPackageComponent (input: {
            owner: "default",
            labbookName: "catbook-package-bad",
            package: "asdfdfghghjfgsdasrftghrty",
            manager: "pip",
            version: "1.0"
          }) {
            clientMutationId
            newPackageComponentEdge {
              node{
                id
                schema
                manager
                package
                version
                fromBase
              }
            }
          }
        }
        """
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(pkg_query))
        assert not os.path.exists(os.path.join(labbook_dir, '.gigantum', 'env', 'package_manager', 'pip_requests.yaml'))

    def test_add_custom_dep(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test adding a custom dependency"""
        lb = LabBook(fixture_working_dir_env_repo_scoped[0])

        labbook_dir = lb.new(name="labbook3", description="my first labbook",
                             owner={"username": "default"})

        # Add a base image
        query = """
        mutation myEnvMutation{
          addCustomComponent(input: {
            owner: "default",
            labbookName: "labbook3",
            repository: "gig-dev_components2",
            componentId: "pillow",
            revision: 0
          }) {
            clientMutationId
            newCustomComponentEdge {
              node{
                id
                repository
                componentId
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

        # Validate the LabBook .gigantum/env/ directory
        assert os.path.exists(os.path.join(labbook_dir, '.gigantum', 'env', 'base')) is True
        assert os.path.exists(os.path.join(labbook_dir, '.gigantum', 'env', 'package_manager')) is True
        assert os.path.exists(os.path.join(labbook_dir, '.gigantum', 'env', 'custom')) is True
        assert os.path.exists(os.path.join(labbook_dir, '.gigantum', 'env', 'entrypoint.sh')) is True

        # Verify file
        component_file = os.path.join(labbook_dir,
                                      '.gigantum',
                                      'env',
                                      'custom',
                                      "gig-dev_components2_pillow.yaml")
        assert os.path.exists(component_file) is True

        # Verify git/notes
        log = lb.git.log()
        assert len(log) == 4
        assert "_GTM_ACTIVITY_START_" in log[0]["message"]
        assert 'pillow' in log[0]["message"]

    def test_remove_package(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test removing a package from a labbook"""
        lb = LabBook(fixture_working_dir_env_repo_scoped[0])

        labbook_dir = lb.new(name="catbook-package-tester-remove", description="LB to test package mutation",
                             owner={"username": "default"})

        # Add a pip package
        pkg_query = """
       mutation myPkgMutation {
         addPackageComponent (input: {
           owner: "default",
           labbookName: "catbook-package-tester-remove",
           package: "docker",
           manager: "pip"
         }) {
           clientMutationId
           newPackageComponentEdge {
             node{
               manager
               package
               fromBase
             }
           }
         }
       }
       """
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(pkg_query))

        # Assert that the dependency was added
        assert os.path.exists(os.path.join(labbook_dir, '.gigantum', 'env', 'package_manager', 'pip_docker.yaml'))

        # Remove a pip package
        pkg_query = """
       mutation myPkgMutation {
         removePackageComponent (input: {
           owner: "default",
           labbookName: "catbook-package-tester-remove",
           package: "docker",
           manager: "pip"
         }) {
           clientMutationId
           success
         }
       }
       """
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(pkg_query))

        # Assert that the dependency is gone
        assert not os.path.exists(os.path.join(labbook_dir, '.gigantum', 'env', 'package_manager', 'pip_docker.yaml'))

    def test_remove_custom_dep(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test removing a custom dependency"""
        lb = LabBook(fixture_working_dir_env_repo_scoped[0])

        labbook_dir = lb.new(name="labbook-remove-custom", description="my first labbook",
                             owner={"username": "default"})

        # Add a custom dep
        query = """
        mutation myEnvMutation{
          addCustomComponent(input: {
            owner: "default",
            labbookName: "labbook-remove-custom",
            repository: "gig-dev_components2",
            componentId: "pillow",
            revision: 0
          }) {
            clientMutationId
            newCustomComponentEdge {
              node{
                repository
                componentId
                revision
                name
                description
              }
            }
          }
        }
        """
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(query))

        # Verify file
        component_file = os.path.join(labbook_dir,
                                      '.gigantum',
                                      'env',
                                      'custom',
                                      "gig-dev_components2_pillow.yaml")
        assert os.path.exists(component_file) is True

        # Remove a custom dep
        query = """
        mutation myEnvMutation{
          removeCustomComponent(input: {
            owner: "default",
            labbookName: "labbook-remove-custom",
            repository: "gig-dev_components2",
            componentId: "pillow"
          }) {
            clientMutationId
            success
          }
        }
        """
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(query))
        assert os.path.exists(component_file) is False
