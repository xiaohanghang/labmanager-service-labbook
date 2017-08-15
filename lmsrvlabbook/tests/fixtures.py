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
import tempfile
import os
import uuid
import shutil
import graphene

from lmcommon.environment import RepositoryManager

from lmsrvlabbook.api.query import LabbookQuery
from lmsrvlabbook.api.mutation import LabbookMutations


# Create ObjectType clases, since the EnvironmentQueries and EnvironmentMutations
# are abstract (allowing multiple inheritance)
class Query(LabbookQuery, graphene.ObjectType):
    pass


class Mutation(LabbookMutations, graphene.ObjectType):
    pass


@pytest.fixture(scope="module")
def schema_and_env_index():
    """A pytest fixture that creates a temporary directory and a config file to match, creates the schema, and builds
    the Environment Component Index
    """
    # Create a temporary working directory
    temp_dir = os.path.join(tempfile.tempdir, uuid.uuid4().hex)
    os.makedirs(temp_dir)

    with tempfile.NamedTemporaryFile(mode="wt") as fp:
        # Write a temporary config file
        fp.write("""core:
  team_mode: false 

environment:
  repo_url:
    - "https://github.com/gig-dev/environment-components.git"

git:
  backend: 'filesystem'
  working_directory: '{}'""".format(temp_dir))
        fp.seek(0)

        # Create test client
        schema = graphene.Schema(query=Query,
                                 mutation=Mutation)

        # get environment data and index
        erm = RepositoryManager(fp.name)
        erm.update_repositories()
        erm.index_repositories()

        yield fp.name, temp_dir, schema  # name of the config file, temporary working directory, the schema

    # Remove the temp_dir
    shutil.rmtree(temp_dir)
