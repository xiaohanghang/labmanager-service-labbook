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
import os
import shutil
import tempfile
import uuid

import docker
import graphene
import pytest
from docker.errors import ImageNotFound
from graphene.test import Client
from mock import patch

from lmcommon.configuration import Configuration
from lmcommon.labbook import LabBook
from lmsrvcore.auth.user import get_logged_in_user

from lmsrvlabbook.api.mutation import LabbookMutations
from lmsrvlabbook.api.query import LabbookQuery


# Create ObjectType clases, since the EnvironmentQueries and EnvironmentMutations
# are abstract (allowing multiple inheritance)
class Query(LabbookQuery, graphene.ObjectType):
    pass


class Mutation(LabbookMutations, graphene.ObjectType):
    pass


@pytest.fixture()
def reset_images():
    """A pytest fixture that checks if the test images exist and deletes them"""
    client = docker.from_env()
    try:
        client.images.get("{}-{}".format(get_logged_in_user(), 'labbook-build'))
        client.images.remove("{}-{}".format(get_logged_in_user(), 'labbook-build'))
    except ImageNotFound:
        pass

    yield None


@pytest.fixture()
def mock_config_file():
    """A pytest fixture that creates a temporary directory and a config file to match. Deletes directory after test"""
    # Create a temporary working directory
    temp_dir = os.path.join(tempfile.tempdir, uuid.uuid4().hex)
    os.makedirs(temp_dir)

    with tempfile.NamedTemporaryFile(mode="wt") as fp:
        # Write a temporary config file
        fp.write("""core:
  team_mode: false 
git:
  backend: 'filesystem'
  working_directory: '{}'""".format(temp_dir))
        fp.seek(0)

        # Create test client
        schema = graphene.Schema(query=Query,
                                 mutation=Mutation)

        yield fp.name, temp_dir, schema  # name of the config file, temporary working directory, the schema

    # Remove the temp_dir
    shutil.rmtree(temp_dir)


class TestLabBookServiceMutations(object):
    def test_build_image(self, reset_images, mock_config_file, snapshot):
        """Test building a labbook's image"""
        # Create labbook
        lb = LabBook(mock_config_file[0])
        lb.new(owner={"username": "default"}, name="labbook-build", description="building an env")

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            # Make and validate request
            client = Client(mock_config_file[2])

            query = """
            {
                labbook(name: "labbook-build", owner: "default") {
                    environment {
                        imageStatus
                        containerStatus
                    }
                }
            }
            """

            snapshot.assert_match(client.execute(query))

            # Build the image
            query = """
            mutation myBuildImage($name: String!){
              buildImage(input: {labbookName: $name}) {
                environment {
                  imageStatus
                  containerStatus
                }
              }
            }
            """
            variables = {"name": "labbook-build"}

            snapshot.assert_match(client.execute(query, variable_values=variables))

            # Get LabBook env status again
            query = """
            {
              labbook(name: "labbook-build", owner: "default") {
                environment {
                    imageStatus
                    containerStatus
                }
              }
            }
            """
            snapshot.assert_match(client.execute(query))
