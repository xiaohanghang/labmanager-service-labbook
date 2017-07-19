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
from snapshottest import snapshot

from graphene.test import Client
import graphene
from mock import patch

from lmcommon.configuration import Configuration
from lmcommon.labbook import LabBook

from lmsrvlabbook.api.query import LabbookQuery
from lmsrvlabbook.api.mutation import LabbookMutations


# Create ObjectType clases, since the LabbookQueries and LabbookMutations are abstract (allowing multiple inheritance)
class Query(LabbookQuery, graphene.ObjectType):
    pass


class Mutation(LabbookMutations, graphene.ObjectType):
    pass


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


class TestNoteService(object):
    # TODO: Add additional testing once services are matured. Currently doesn't check any fields that can change
    # between tests (e.g. commit, linked_commit, datetime)
    def test_create_note(self, mock_config_file, snapshot):
        """Test creating and getting a note"""

        # Create labbook
        lb = LabBook(mock_config_file[0])
        lb.new(owner={"username": "default"}, name="notes-test-1", description="my first labbook10000")

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            # Make and validate request
            client = Client(mock_config_file[2])

            # Create a file in the LabBook and commit it
            working_dir = lb.git.config["working_directory"]
            labbook_dir = os.path.join(working_dir, "default", "default", "notes-test-1")
            with open(os.path.join(labbook_dir, "code", "test1.txt"), 'wt') as dt:
                dt.write("Some content")
            lb.git.add(os.path.join(labbook_dir, "code", "test1.txt"))
            commit = lb.git.commit("a test commit")

            # Create a note
            query = """
            mutation makenote {
              createNote(input: {
                labbookName: "notes-test-1",
                owner: "default",
                level: USER_MINOR,
                message: "Added a new file in this test",
                linkedCommit: \"""" + str(commit) + """\",
                tags: ["user", "minor"],
                freeText: "Lots of stuff can go here <>><<>::SDF:",
                objects: [{key: "objectkey1", objectType: "PNG", value: "2new0x7FABC374FX"}]
              })
              {
                note {
                  message
                  commit
                }
              }
            }
            """

            result = client.execute(query)

            # Get Note you just created
            note_commit = result["data"]["createNote"]["note"]["commit"]

            query = """
            {
                labbook(name: "notes-test-1", owner: "default") {
                    notes(first:1) {
                        edges {
                            node {
                                message
                            }
                        }
                    }
                }
            }
            """
            snapshot.assert_match(client.execute(query))

    def test_get_note_summaries(self, mock_config_file, snapshot):
        """Test creating and getting a note"""

        # Create labbook
        lb = LabBook(mock_config_file[0])
        lb.new(owner={"username": "default"}, name="notes-test-2", description="my first labbook10000")

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            # Make and validate request
            client = Client(mock_config_file[2])

            # Create a file in the LabBook and commit it
            working_dir = lb.git.config["working_directory"]
            labbook_dir = os.path.join(working_dir, "default", "default", "notes-test-2")
            with open(os.path.join(labbook_dir, "code", "test1.txt"), 'wt') as dt:
                dt.write("Some content")
            lb.git.add(os.path.join(labbook_dir, "code", "test1.txt"))
            commit = lb.git.commit("a test commit")

            for cnt in range(0, 5):
                # Create a note
                query = """
                        mutation CreateNote {
                          createNote(labbookName: "notes-test-2",
                            message: "Added a new file in this test """ + str(cnt) + """\",
                            level: USER_MINOR,
                            linkedCommit: \"""" + str(commit) + """\",
                            tags: ["user", "minor"],
                            freeText: "Lots of stuff can go here <>><<>::SDF:",
                            objects: [{key: "objectkey1", objectType: "PNG", value: "2new0x7FABC374FX"}]) {
                            note {
                              labbookName                  
                              author 
                              message
                              level
                              tags                  
                              freeText
                              objects {
                                key
                                objectType
                                value
                              }
                            }
                          }
                        }
                        """

                snapshot.assert_match(client.execute(query))

            # Get Note you just created
            query = """
            {
              noteSummaries(labbookName: "notes-test-2") {
                entries {
                  labbookName
                  author
                  level
                  message
                  tags
                }
              }
            }
            """
            snapshot.assert_match(client.execute(query))
