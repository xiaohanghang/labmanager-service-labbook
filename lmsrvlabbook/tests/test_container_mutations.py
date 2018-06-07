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
import time

from lmsrvlabbook.tests.fixtures import fixture_working_dir, fixture_working_dir_env_repo_scoped, \
    build_image_for_jupyterlab

from lmcommon.container.container import ContainerOperations


class TestContainerMutations(object):
    def test_start_stop_container(self, build_image_for_jupyterlab):
        """Test start stop mutations"""
        query = """
           {
               labbook(name: "containerunittestbook", owner: "unittester") {
                   environment {
                       imageStatus
                       containerStatus
                   }
               }
           }
           """
        r = build_image_for_jupyterlab[4].execute(query)
        assert 'errors' not in r
        assert r['data']['labbook']['environment']['imageStatus'] == 'EXISTS'
        assert r['data']['labbook']['environment']['containerStatus'] == 'NOT_RUNNING'

        try:
            # Start the container
            start_query = """
               mutation myStart {
                 startContainer(input: {labbookName: "containerunittestbook", owner: "unittester"}) {
                   environment {
                     imageStatus
                     containerStatus
                   }
                 }
               }
               """
            r = build_image_for_jupyterlab[4].execute(start_query)
            assert r['data']['startContainer']['environment']['imageStatus'] == 'EXISTS'
            assert r['data']['startContainer']['environment']['containerStatus'] == 'RUNNING'

            # TEST GIG-909: Prevent rebuilding images when container for LB already running
            build_q = """
                mutation myBuild {
                    buildImage(input: {
                        labbookName: "containerunittestbook",
                        owner: "unittester"
                    }) {
                        environment {
                            imageStatus
                            containerStatus
                        }                        
                    }
                }
            """
            r = build_image_for_jupyterlab[4].execute(build_q)
            assert 'errors' in r # Yes, we really want to check that the errors key exists
            assert 'Cannot build image for running container' in r['errors'][0]['message']
            assert not r['data']['buildImage'] # Yes, this should be empty due to failuire.

            # Stop the container
            stop_query = """
               mutation myStop {
                 stopContainer(input: {labbookName: "containerunittestbook", owner: "unittester"}) {
                   environment {
                     imageStatus
                     containerStatus
                   }
                 }
               }
               """
            r = build_image_for_jupyterlab[4].execute(stop_query)
            assert 'errors' not in r
            assert r['data']['stopContainer']['environment']['imageStatus'] == 'EXISTS'
            assert r['data']['stopContainer']['environment']['containerStatus'] == 'NOT_RUNNING'

        except:
            try:
                # Mutation failed. Container *might* have stopped, but try to stop it just in case
                build_image_for_jupyterlab[2].containers.get('gmlb-unittester-unittester-containerunittestbook').stop(timeout=4)
            except:
                # Make a best effort
                pass
            raise
        finally:
            try:
                # Remove the container.
                build_image_for_jupyterlab[2].containers.get('gmlb-unittester-unittester-containerunittestbook').remove()
            except:
                # Make a best effort
                pass

    @pytest.mark.skipif(getpass.getuser() == 'circleci', reason="Cannot run this networking test in CircleCI environment")
    def test_start_jupyterlab(self, build_image_for_jupyterlab):
        """Test listing labbooks"""
        # Start the container
        lb, container_id, port_maps = ContainerOperations.start_container(build_image_for_jupyterlab[0],
                                                                          username='unittester')

        try:
            lb = build_image_for_jupyterlab[0]
            docker_client = build_image_for_jupyterlab[2]
            client = build_image_for_jupyterlab[4]

            q = f"""
            mutation x {{
                startDevTool(input: {{
                    owner: "{lb.owner['username']}",
                    labbookName: "{lb.name}",
                    devTool: "jupyterlab"
                }}) {{
                    path
                    }}

            }}
            """
            r = client.execute(q)
            assert 'errors' not in r

            assert ':8890/lab' in r['data']['startDevTool']['path']
            l = [a for a in docker_client.containers.get(container_id=container_id).exec_run(
                'sh -c "ps aux | grep jupyter-lab | grep -v \' grep \'"', user='giguser').decode().split('\n') if a]
            assert len(l) == 1
        finally:
            # Remove the container you fired up
            build_image_for_jupyterlab[2].containers.get(container_id=container_id).stop(timeout=10)
            build_image_for_jupyterlab[2].containers.get(container_id=container_id).remove()
