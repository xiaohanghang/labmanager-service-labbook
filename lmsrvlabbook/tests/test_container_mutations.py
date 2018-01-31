# Copyright (c) 2018 FlashX, LLC
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
import getpass
import os
import time
import shutil

from snapshottest import snapshot

from lmsrvlabbook.tests.fixtures import fixture_working_dir, fixture_working_dir_env_repo_scoped

from lmcommon.configuration import get_docker_client
from lmcommon.fixtures import (ENV_UNIT_TEST_REPO, ENV_UNIT_TEST_REV, ENV_UNIT_TEST_BASE)
from lmcommon.labbook import LabBook
from lmcommon.labbook.operations import ContainerOps
from lmcommon.environment import ComponentManager
from lmcommon.imagebuilder import ImageBuilder


@pytest.fixture(scope='class')
def build_lb_image_for_jupyterlab(fixture_working_dir_env_repo_scoped):
    # Create a labook
    lb = LabBook(fixture_working_dir_env_repo_scoped[0])
    lb.new(name="jup-container-testlb", description="Testing docker building.", owner={"username": "default"})

    # Create Component Manager
    cm = ComponentManager(lb)
    # Add a component
    cm.add_component("base", ENV_UNIT_TEST_REPO, ENV_UNIT_TEST_BASE, ENV_UNIT_TEST_REV)
    n = cm.add_package("pip3", "requests", "2.18.4")

    ib = ImageBuilder(lb.root_dir)
    docker_lines = ib.assemble_dockerfile(write=True)
    assert 'RUN pip3 install requests==2.18.4' in docker_lines
    assert all(['==None' not in l for l in docker_lines.split()])
    unit_test_tag = "default-default-jup-container-testlb"
    docker_client = get_docker_client()

    assert os.path.exists(os.path.join(lb.root_dir, '.gigantum', 'env', 'entrypoint.sh'))

    docker_image_id = ib.build_image(docker_client=docker_client, image_tag=unit_test_tag,
                                     nocache=False, username="default", assemble=False)['docker_image_id']

    yield lb, ib, docker_client, docker_image_id, fixture_working_dir_env_repo_scoped[2]

    # remove labbook
    shutil.rmtree(lb.root_dir)


class TestContainerMutations(object):
    @pytest.mark.skipif(getpass.getuser() == 'circleci', reason="Cannot build images on CircleCI")
    def test_start_stop_container(self, build_lb_image_for_jupyterlab, snapshot):
        """Test start stop mutations"""
        query = """
           {
               labbook(name: "jup-container-testlb", owner: "default") {
                   environment {
                       imageStatus
                       containerStatus
                   }
               }
           }
           """
        snapshot.assert_match(build_lb_image_for_jupyterlab[4].execute(query))

        # Start the container
        start_query = """
           mutation myBuildImage {
             startContainer(input: {labbookName: "jup-container-testlb", owner: "default"}) {
               environment {
                 imageStatus
                 containerStatus
               }
             }
           }
           """
        snapshot.assert_match(build_lb_image_for_jupyterlab[4].execute(start_query))

        # Wait for start to succeed for up to 30 seconds
        success = False
        for _ in range(10):
            result = build_lb_image_for_jupyterlab[4].execute(query)

            if result['data']['labbook']['environment']['containerStatus'] == 'RUNNING':
                success = True
                break

            time.sleep(1)

        assert success is True, "Failed to start within 10 second timeout."
        snapshot.assert_match(build_lb_image_for_jupyterlab[4].execute(query))

        try:
            # Stop the container
            stop_query = """
               mutation myBuildImage {
                 stopContainer(input: {labbookName: "jup-container-testlb", owner: "default"}) {
                   environment {
                     imageStatus
                     containerStatus
                   }
                 }
               }
               """
            snapshot.assert_match(build_lb_image_for_jupyterlab[4].execute(stop_query))
            assert 1==2
            # Wait for start to succeed for up to 30 seconds
            success = False
            for _ in range(10):
                result = build_lb_image_for_jupyterlab[4].execute(query)

                if result['data']['labbook']['environment']['containerStatus'] == 'NOT_RUNNING':
                    success = True
                    break

                time.sleep(1)

            assert success is True, "Failed to start within 10 second timeout."
            snapshot.assert_match(build_lb_image_for_jupyterlab[4].execute(query))

        except:
            build_lb_image_for_jupyterlab[2].containers.get(tag="").stop(timeout=4)

    @pytest.mark.skipif(getpass.getuser() == 'circleci', reason="Cannot build images on CircleCI")
    def test_start_jupyterlab(self, build_lb_image_for_jupyterlab):
        """Test listing labbooks"""
        # Start the container
        lb, keys, port_maps = ContainerOps.start_container(build_lb_image_for_jupyterlab[0],
                                                           override_docker_image=build_lb_image_for_jupyterlab[3])
        container_id = keys['docker_container_id']

        try:
            lb = build_lb_image_for_jupyterlab[0]
            docker_client = build_lb_image_for_jupyterlab[2]
            client = build_lb_image_for_jupyterlab[4]

            q = f"""
            mutation x {{
                startDevTool(input: {{
                    owner: "{lb.owner['username']}",
                    labbookName: "{lb.name}",
                    devTool: "jupyterlab",
                    containerOverrideId: "{container_id}"
                }}) {{
                    path
                }}
            }}
            """
            r = client.execute(q)
            assert 'errors' not in r

            assert ':8888/lab' in r['data']['startDevTool']['path']
            l = [a for a in docker_client.containers.get(container_id=container_id).exec_run(
                'sh -c "ps aux | grep jupyter-lab | grep -v \' grep \'"', user='giguser').decode().split('\n') if a]
            assert len(l) == 1
        finally:
            # Remove the container you fired up
            build_lb_image_for_jupyterlab[2].containers.get(container_id=container_id).stop(timeout=4)
            build_lb_image_for_jupyterlab[2].containers.get(container_id=container_id).remove()
