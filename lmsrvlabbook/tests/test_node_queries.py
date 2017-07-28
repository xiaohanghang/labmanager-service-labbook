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

from lmcommon.labbook import LabBook
from lmcommon.configuration import Configuration

from ..api import LabbookMutations, LabbookQuery


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


def create_stock_labbook(client, name: str, desc: str = "Example labbook by mutation."):
    """Creates a boilerplate labbook for further queries or mutations"""

    query = """
    mutation myCreateLabbook($name: String!, $desc: String!) {
      createLabbook(input: {name: $name, description: $desc}) {
        labbook {
          id
          name
          description
        }
      }
    }
    """

    variables = {"name": name, "desc": desc}
    results = client.execute(query, variable_values=variables)
    return results


class TestLabBookServiceQueries(object):

    def test_node_labbook_from_object(self, mock_config_file, snapshot):
        lb = LabBook(mock_config_file[0])
        lb.new(owner={"username": "default"}, name="cat-lab-book1", description="Test cat labbook from obj")

        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            # Make and validate request
            client = Client(mock_config_file[2])

            query = """
                    {
                        node(id: "TGFiYm9vazpkZWZhdWx0JmNhdC1sYWItYm9vazE=") {
                            ... on Labbook {
                                name
                                description
                                activeBranch {
                                    name
                                }
                            }
                            id
                        }
                    }
                    """

            snapshot.assert_match(client.execute(query))

    def test_node_labbook_from_mutation(self, mock_config_file, snapshot):
        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            # Make and validate request
            client = Client(mock_config_file[2])

            create_query = """
            mutation myCreateLabbook($name: String!, $desc: String!) {
              createLabbook(input: {name: $name, description: $desc}) {
                labbook {
                  id
                  name
                  description
                }
              }
            }
            """

            variables = {"name": "test-lab-book1", "desc": "my test description"}
            labbook_id = \
                client.execute(create_query, variable_values=variables)['data']['createLabbook']['labbook']['id']

            query = """
                    {
                        node(id: "%s") {
                            ... on Labbook {
                                name
                                description
                                activeBranch {
                                    name
                                }
                            }
                            id
                        }
                    }
                    """ % labbook_id

            snapshot.assert_match(client.execute(query))

    def test_node_environment(self, mock_config_file, snapshot):

        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            client = Client(mock_config_file[2])
            create_stock_labbook(client, "node-env-test-lb", "Example labbook by mutation.")

            env_query = """
            {
                node(id: "TGFiYm9vazpkZWZhdWx0Jm5vZGUtZW52LXRlc3QtbGI=") {
                    id
                    ... on Labbook {
                        name
                        description
                        environment {
                            id
                            imageStatus
                            containerStatus
                        }
                    }
                }
            }
            """
            results = client.execute(env_query)
            snapshot.assert_match(results)

            env_id = results['data']['node']['environment']['id']

            env_node_query = """
            {
                node(id: "%s") {
                    id
                    ... on Environment {
                        imageStatus
                        containerStatus
                    }
                }
            }
            """ % env_id
            snapshot.assert_match(client.execute(env_node_query))

    def test_node_notes(self, mock_config_file, snapshot):
        labbook_name="test-node-note-1"

        lb = LabBook(mock_config_file[0])
        lb.new(owner={"username": "default"}, name=labbook_name, description="Labby McLabbook 99")

        with patch.object(Configuration, 'find_default_config', lambda self: mock_config_file[0]):
            client = Client(mock_config_file[2])

            working_dir = lb.git.config["working_directory"]
            labbook_dir = os.path.join(working_dir, "default", "default", "labbooks", labbook_name)
            with open(os.path.join(labbook_dir, "code", "test1.txt"), 'wt') as dt:
                dt.write("Some content")
            lb.git.add(os.path.join(labbook_dir, "code", "test1.txt"))
            commit = lb.git.commit("a test commit")

            #results = create_stock_labbook(client=client, name=labbook_name)

            make_note_query = """
             mutation makenote {
               createNote(input: {
                 labbookName: \"""" + labbook_name + """\",
                 owner: "default",
                 level: USER_MINOR,
                 message: "Added a new file in this test",
                 linkedCommit: \"""" + str(commit) + """\",
                 tags: ["user", "minor"],
                 freeText: "Lots of stuff can go here <>><<>::SDF:",
                 objects: [{key: "objectkey1",
                            type: "PNG", 
                            value: "2new0x7FABC374FX"
                            }, 
                            {key: "objectkey2", 
                            type: "BLOB", 
                            value: "YXNkZmFzZGZmZ2RoYXNkMTI0Mw=="}]
               })
               {
                 note {
                   id
                   message              
                 }
               }
             }
             """
            response = client.execute(make_note_query)

            query = """
            {
                labbook(name: "%s", owner: "default") {
                    notes(first: 1) {
                        edges {
                            node {                                                                                       
                                id
                                author
                                level
                            }
                            cursor
                        }                        
                    }
                }
            }
            """ % labbook_name
            first_note_id = client.execute(query)['data']['labbook']['notes']['edges'][0]['node']['id']

            #import pprint; pprint.pprint(first_note_id); assert False
            node_note_query = """
            {
                node(id: "%s") {
                    ... on Note {
                        author
                        level
                        message
                        tags
                    }
                }
            }
            """ % first_note_id

            snapshot.assert_match(client.execute(node_note_query))
