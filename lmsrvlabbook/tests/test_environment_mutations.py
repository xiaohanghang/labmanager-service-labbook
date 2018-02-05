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
import time
from docker.errors import ImageNotFound
import getpass

from lmcommon.configuration import get_docker_client
from lmcommon.labbook import LabBook
from lmsrvlabbook.tests.fixtures import fixture_working_dir_env_repo_scoped
from lmsrvcore.auth.user import get_logged_in_username
from lmcommon.environment import ComponentManager


@pytest.fixture
def reset_images(request):
    """A pytest fixture that checks if the test images exist and deletes them"""
    # Clean up images
    client = get_docker_client()

    # image should never exist before the test starts
    image_name = "gmlb-{}-{}".format(get_logged_in_username(), f'default-{request.param}')
    try:
        client.images.get(image_name)
        client.images.remove(image_name)
        raise ValueError("Test image exists before test started. Attempting to automatically removing image. Run again")
    except ImageNotFound:
        pass

    yield None

    try:
        client.images.get(image_name)
        client.images.remove(image_name)
    except ImageNotFound:
        pass


class TestEnvironmentMutations(object):
    @pytest.mark.skipif(getpass.getuser() == 'circleci', reason="Cannot build images on CircleCI")
    @pytest.mark.parametrize('reset_images', ["labbook-build1"], indirect=['reset_images'])
    def test_build_image(self, fixture_working_dir_env_repo_scoped, reset_images):
        """Test building a labbook's image"""
        # Create labbook
        lb = LabBook(fixture_working_dir_env_repo_scoped[0])
        lb.new(owner={"username": "default"}, name="labbook-build1", description="building an env")
        # add a base
        cm = ComponentManager(lb)
        cm.add_component("base", "gig-dev_components2", "ut-busybox", 0)

        query = """
        {
            labbook(name: "labbook-build1", owner: "default") {
                environment {
                    imageStatus
                    containerStatus
                }
            }
        }
        """

        r = fixture_working_dir_env_repo_scoped[2].execute(query)
        assert 'errors' not in r
        assert r['data']['labbook']['environment']['imageStatus'] == 'DOES_NOT_EXIST'
        assert r['data']['labbook']['environment']['containerStatus'] == 'NOT_RUNNING'

        # Build the image
        build_query = """
        mutation myBuildImage {
          buildImage(input: {labbookName: "labbook-build1", owner: "default"}) {
            environment {
              imageStatus
              containerStatus
            }
          }
        }
        """
        r = fixture_working_dir_env_repo_scoped[2].execute(build_query)
        import pprint;
        pprint.pprint(r)
        assert 'errors' not in r

        assert r['data']['buildImage']['environment']['imageStatus'] == 'BUILD_IN_PROGRESS'
        assert r['data']['buildImage']['environment']['containerStatus'] == 'NOT_RUNNING'

        # Wait for build to succeed for up to 30 seconds
        success = False
        for _ in range(30):
            result = fixture_working_dir_env_repo_scoped[2].execute(query)

            if result['data']['labbook']['environment']['imageStatus'] == 'EXISTS':
                success = True
                break

            time.sleep(1)

        assert success is True, "Failed to build within 30 second timeout."

        r = fixture_working_dir_env_repo_scoped[2].execute(query)
        assert 'errors' not in r
        assert r['data']['labbook']['environment']['imageStatus'] == 'EXISTS'
        assert r['data']['labbook']['environment']['containerStatus'] == 'NOT_RUNNING'

    @pytest.mark.skipif(getpass.getuser() == 'circleci', reason="Cannot build images on CircleCI")
    @pytest.mark.parametrize('reset_images', ["labbook-build2"], indirect=['reset_images'])
    def test_build_image_no_cache(self, fixture_working_dir_env_repo_scoped, reset_images):
        """Test building a labbook's image"""
        # Create labbook
        lb = LabBook(fixture_working_dir_env_repo_scoped[0])
        lb.new(owner={"username": "default"}, name="labbook-build2", description="building an env")
        # add a base
        cm = ComponentManager(lb)
        cm.add_component("base", "gig-dev_components2", "ut-busybox", 0)

        query = """
        {
            labbook(name: "labbook-build2", owner: "default") {
                environment {
                    imageStatus
                    containerStatus
                }
            }
        }
        """

        r = fixture_working_dir_env_repo_scoped[2].execute(query)
        assert 'errors' not in r
        assert r['data']['labbook']['environment']['imageStatus'] == 'DOES_NOT_EXIST'
        assert r['data']['labbook']['environment']['containerStatus'] == 'NOT_RUNNING'

        # Build the image
        build_query = """
        mutation myBuildImage {
          buildImage(input: {labbookName: "labbook-build2", owner: "default", noCache: true}) {
            environment {
              imageStatus
              containerStatus
            }
          }
        }
        """
        r = fixture_working_dir_env_repo_scoped[2].execute(build_query)
        assert 'errors' not in r
        assert r['data']['buildImage']['environment']['imageStatus'] == 'BUILD_IN_PROGRESS'
        assert r['data']['buildImage']['environment']['containerStatus'] == 'NOT_RUNNING'

        # Wait for build to succeed for up to 30 seconds
        success = False
        for _ in range(30):
            result = fixture_working_dir_env_repo_scoped[2].execute(query)

            if result['data']['labbook']['environment']['imageStatus'] == 'EXISTS':
                success = True
                break

            time.sleep(1)

        assert success is True, "Failed to build within 30 second timeout."


        r= fixture_working_dir_env_repo_scoped[2].execute(query)
        assert 'errors' not in r
        assert r['data']['labbook']['environment']['imageStatus'] == 'EXISTS'
        assert r['data']['labbook']['environment']['containerStatus'] == 'NOT_RUNNING'


