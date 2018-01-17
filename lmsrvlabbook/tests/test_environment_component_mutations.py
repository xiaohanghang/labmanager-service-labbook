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
from graphene.test import Client
from mock import patch

from lmsrvlabbook.tests.fixtures import fixture_working_dir_env_repo_scoped
from lmcommon.configuration import Configuration
from lmcommon.labbook import LabBook


class TestAddComponentMutations(object):
    def test_add_base_image(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test listing labbooks"""
        lb = LabBook(fixture_working_dir_env_repo_scoped[0])

        labbook_dir = lb.new(name="labbook1", description="my first labbook",
                             owner={"username": "default"})

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_env_repo_scoped[0]):
            # Make and validate request
            client = Client(fixture_working_dir_env_repo_scoped[2])

            # Add a base image
            query = """
            mutation myEnvMutation{
              addEnvironmentComponent(input: {
                componentClass: base_image,
                repository: "gig-dev_environment-components",
                namespace: "gigantum",
                component: "ubuntu1604-python3",
                version: "0.4",
                labbookName: "labbook1"
              }) {
                clientMutationId
                environmentComponent {
                    name
                }
              }
            }
            """
            result = client.execute(query)

        assert result['data']['addEnvironmentComponent']['environmentComponent']['name'] == 'ubuntu1604-python3'

        # Validate the LabBook .gigantum/env/ directory
        assert os.path.exists(os.path.join(labbook_dir, '.gigantum', 'env', 'base_image')) is True
        assert os.path.exists(os.path.join(labbook_dir, '.gigantum', 'env', 'dev_env')) is True
        assert os.path.exists(os.path.join(labbook_dir, '.gigantum', 'env', 'package_manager')) is True
        assert os.path.exists(os.path.join(labbook_dir, '.gigantum', 'env', 'custom')) is True
        assert os.path.exists(os.path.join(labbook_dir, '.gigantum', 'env', 'entrypoint.sh')) is True

        # Verify file
        component_file = os.path.join(labbook_dir,
                                      '.gigantum',
                                      'env',
                                      'base_image',
                                      "gig-dev_environment-components_gigantum_ubuntu1604-python3.yaml")
        assert os.path.exists(component_file) is True

        with open(component_file, 'rt') as cf:
            data = yaml.load(cf)

        assert data['info']['name'] == 'ubuntu1604-python3'
        assert data['info']['version_major'] == 0
        assert data['info']['version_minor'] == 4
        assert data['image']['namespace'] == 'gigdev'
        assert data['image']['repo'] == 'ubuntu1604-python3'
        assert data['###namespace###'] == 'gigantum'

        # Verify git/notes
        log = lb.git.log()
        assert len(log) == 4
        assert "_GTM_ACTIVITY_START_" in log[0]["message"]
        assert 'ubuntu1604-python3' in log[0]["message"]

    def test_add_dev_env(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test listing labbooks"""
        lb = LabBook(fixture_working_dir_env_repo_scoped[0])

        labbook_dir = lb.new(name="labbook2", description="my first labbook",
                             owner={"username": "default"})

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_env_repo_scoped[0]):
            # Make and validate request
            client = Client(fixture_working_dir_env_repo_scoped[2])

            # Add a base image
            query = """
            mutation myEnvMutation{
              addEnvironmentComponent(input: {componentClass: dev_env,
              repository: "gig-dev_environment-components",
              namespace: "gigantum", component: "jupyter-ubuntu",
              version: "0.1", labbookName: "labbook2"}) {
                clientMutationId
              }
            }
            """
            client.execute(query)

        # Validate the LabBook .gigantum/env/ directory
        assert os.path.exists(os.path.join(labbook_dir, '.gigantum', 'env', 'base_image')) is True
        assert os.path.exists(os.path.join(labbook_dir, '.gigantum', 'env', 'dev_env')) is True
        assert os.path.exists(os.path.join(labbook_dir, '.gigantum', 'env', 'package_manager')) is True
        assert os.path.exists(os.path.join(labbook_dir, '.gigantum', 'env', 'custom')) is True
        assert os.path.exists(os.path.join(labbook_dir, '.gigantum', 'env', 'entrypoint.sh')) is True

        # Verify file
        component_file = os.path.join(labbook_dir,
                                      '.gigantum',
                                      'env',
                                      'dev_env',
                                      "gig-dev_environment-components_gigantum_jupyter-ubuntu.yaml")
        assert os.path.exists(component_file) is True

        with open(component_file, 'rt') as cf:
            data = yaml.load(cf)

        assert data['info']['name'] == 'jupyter-ubuntu'
        assert data['info']['version_major'] == 0
        assert data['info']['version_minor'] == 1
        assert data['###namespace###'] == 'gigantum'
        assert len(data['install_commands']) == 1
        assert data['install_commands'][0] == 'pip3 install jupyter'
        assert "exec_commands" in data
        assert "exposed_tcp_ports" in data

        # Verify git/notes
        log = lb.git.log()
        assert len(log) == 4
        assert "_GTM_ACTIVITY_START_" in log[0]["message"]
        assert 'jupyter-ubuntu' in log[0]["message"]

    def test_add_package(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test listing labbooks"""
        lb = LabBook(fixture_working_dir_env_repo_scoped[0])

        labbook_dir = lb.new(name="catbook-package-tester", description="LB to test package mutation",
                             owner={"username": "default"})

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_env_repo_scoped[0]):
            # Make and validate request
            client = Client(fixture_working_dir_env_repo_scoped[2])

            # Add a base image
            query = """
            mutation myEnvMutation{
              addEnvironmentComponent(input: {
                componentClass: dev_env,
                repository: "gig-dev_environment-components",
                namespace: "gigantum", component: "jupyter-ubuntu",
                version: "0.1",
                labbookName: "catbook-package-tester"
              }) {
                clientMutationId
              }
            }
            """
            client.execute(query)

            # Add a base image
            pkg_query = """
            mutation myPkgMutation {
              addEnvironmentPackage(input: {
                labbookName: "catbook-package-tester",
                packageName: "docker",
                packageManager: "apt"
              }) {
                clientMutationId
                environmentPackage {
                    packageName
                    packageManager
                }
              }
            }
            """
            result = client.execute(pkg_query)

        import pprint; pprint.pprint(result)
        assert result['data']['addEnvironmentPackage']['environmentPackage']['packageName'] == 'docker'
        assert result['data']['addEnvironmentPackage']['environmentPackage']['packageManager'] == 'apt'

        # Validate the LabBook .gigantum/env/ directory
        assert os.path.exists(os.path.join(labbook_dir, '.gigantum', 'env', 'package_manager')) is True

        assert os.path.exists(os.path.join(labbook_dir, '.gigantum', 'env', 'package_manager', 'apt_docker.yaml'))

        with open(os.path.join(labbook_dir, '.gigantum', 'env', 'package_manager', 'apt_docker.yaml')) as pkg_yaml:
            package_info_dict = yaml.load(pkg_yaml)

            assert package_info_dict['name'] == 'docker'
            assert package_info_dict['package_manager'] == 'apt'

    def test_add_custom_dep(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test adding a custom dependency"""
        lb = LabBook(fixture_working_dir_env_repo_scoped[0])

        labbook_dir = lb.new(name="labbook3", description="my first labbook",
                             owner={"username": "default"})

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_env_repo_scoped[0]):
            # Make and validate request
            client = Client(fixture_working_dir_env_repo_scoped[2])

            # Add a base image
            query = """
            mutation myEnvMutation{
              addEnvironmentComponent(input: {componentClass: custom,
              repository: "gig-dev_environment-components",
              namespace: "gigantum", component: "ubuntu-python3-pillow",
              version: "0.3", labbookName: "labbook3"}) {
                clientMutationId
              }
            }
            """
            client.execute(query)

        # Validate the LabBook .gigantum/env/ directory
        assert os.path.exists(os.path.join(labbook_dir, '.gigantum', 'env', 'base_image')) is True
        assert os.path.exists(os.path.join(labbook_dir, '.gigantum', 'env', 'dev_env')) is True
        assert os.path.exists(os.path.join(labbook_dir, '.gigantum', 'env', 'package_manager')) is True
        assert os.path.exists(os.path.join(labbook_dir, '.gigantum', 'env', 'custom')) is True
        assert os.path.exists(os.path.join(labbook_dir, '.gigantum', 'env', 'entrypoint.sh')) is True

        # Verify file
        component_file = os.path.join(labbook_dir,
                                      '.gigantum',
                                      'env',
                                      'custom',
                                      "gig-dev_environment-components_gigantum_ubuntu-python3-pillow.yaml")
        assert os.path.exists(component_file) is True

        with open(component_file, 'rt') as cf:
            data = yaml.load(cf)

        assert data['info']['name'] == 'ubuntu-python3-pillow'
        assert data['info']['version_major'] == 0
        assert data['info']['version_minor'] == 3
        assert data['###namespace###'] == 'gigantum'
        assert "docker" in data

        # Verify git/notes
        log = lb.git.log()
        assert len(log) == 4
        assert "_GTM_ACTIVITY_START_" in log[0]["message"]
        assert 'ubuntu-python3-pillow' in log[0]["message"]
