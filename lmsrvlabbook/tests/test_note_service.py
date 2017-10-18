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
import os
from snapshottest import snapshot
from lmsrvlabbook.tests.fixtures import fixture_working_dir

from graphene.test import Client
import graphene
from mock import patch

from lmcommon.configuration import Configuration
from lmcommon.labbook import LabBook


class TestNoteService(object):
    # TODO: Add additional testing once services are matured. Currently doesn't check any fields that can change
    # between tests (e.g. commit, linked_commit, datetime)
    def test_create_note(self, fixture_working_dir, snapshot):
        """Test creating and getting a note"""

        # Create labbook
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="notes-test-1", description="my first labbook10000")

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir[0]):
            # Make and validate request
            client = Client(fixture_working_dir[2])

            # Create a file in the LabBook and commit it
            working_dir = lb.git.config["working_directory"]
            labbook_dir = os.path.join(working_dir, "default", "default", "labbooks", "notes-test-1")
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
                objects: [{key: "objectkey1", type: "PNG", value: "2new0x7FABC374FX"}]
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

    def test_get_note_summaries(self, fixture_working_dir, snapshot):
        """Test creating and getting a note"""

        # Create labbook
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="notes-test-2", description="my first labbook10000")

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir[0]):
            # Make and validate request
            client = Client(fixture_working_dir[2])

            # Create a file in the LabBook and commit it
            working_dir = lb.git.config["working_directory"]
            labbook_dir = os.path.join(working_dir, "default", "default", "labbooks", "notes-test-2")

            for cnt in range(0, 5):
                with open(os.path.join(labbook_dir, "code", "test{}.txt".format(cnt)), 'wt') as dt:
                    dt.write("Some content")
                lb.git.add(os.path.join(labbook_dir, "code", "test{}.txt".format(cnt)))
                commit = lb.git.commit("a test commit {}".format(cnt))

                # Create a note
                query = """
                        mutation CreateNote {
                          createNote(input: {
                            labbookName: "notes-test-2",
                            message: "Added a new file in this test """ + str(cnt) + """\",
                            level: USER_MINOR,
                            linkedCommit: \"""" + str(commit) + """\",
                            tags: ["user", "minor"],
                            freeText: "Lots of stuff can go here <>><<>::SDF:",
                            objects: [{key: "objectkey1", type: "PNG", value: "2new0x7FABC374FX"}]}) {
                                note {                  
                                  author 
                                  message
                                  level
                                  tags                  
                                  freeText
                                }
                            }
                          }
                        
                        """

                snapshot.assert_match(client.execute(query))

            # Get Note you just created
            query = """
            {
              labbook(name: "notes-test-2", owner: "default") {
                notes {
                    edges {
                        node {
                            message
                            author
                            level
                            tags
                        }
                    }
                }
              }
            }
            """
            snapshot.assert_match(client.execute(query))

    def test_get_full_note(self, fixture_working_dir, snapshot):
        """Test creating and getting a note"""

        # Create labbook
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="notes-test-1", description="my first labbook10000")

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir[0]):
            # Make and validate request
            client = Client(fixture_working_dir[2])

            # Create a file in the LabBook and commit it
            working_dir = lb.git.config["working_directory"]
            labbook_dir = os.path.join(working_dir, "default", "default", "labbooks", "notes-test-1")
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
                objects: [{key: "objectkey1", type: "PNG", value: "2new0x7FABC374FX"}, {key: "objectkey2", type: "BLOB", value: "YXNkZmFzZGZmZ2RoYXNkMTI0Mw=="}]
              })
              {
                note {
                  message              
                }
              }
            }
            """

            result = client.execute(query)

            query = """
            {
                labbook(name: "notes-test-1", owner: "default") {
                    notes(first:1) {
                        edges {
                            node {                                                                                       
                                message
                                author
                                level
                                tags
                                freeText
                                objects {
                                    edges {
                                        node {
                                            key
                                            type
                                            value
                                        }
                                        cursor
                                    }
                                }
                            }
                            cursor
                        }                        
                    }
                }
            }
            """
            response = client.execute(query)
            snapshot.assert_match(response)

            query = """
                       {
                           labbook(name: "notes-test-1", owner: "default") {
                               notes(first:1) {
                                   edges {
                                       node {
                                           id                                                       
                                           commit
                                           linkedCommit        
                                           timestamp                                   
                                       }
                                       cursor
                                   }                        
                               }
                           }
                       }
                       """
            response = client.execute(query)

            # make sure fields that do change are at least reasonable
            assert type(response['data']['labbook']['notes']['edges'][0]['node']['commit']) == str
            assert type(response['data']['labbook']['notes']['edges'][0]['node']['linkedCommit']) == str
            assert type(response['data']['labbook']['notes']['edges'][0]['node']['timestamp']) == str
            assert len(response['data']['labbook']['notes']['edges'][0]['node']['commit']) == 40
            assert len(response['data']['labbook']['notes']['edges'][0]['node']['linkedCommit']) == 40

    def test_get_required_note(self, fixture_working_dir, snapshot):
        """Test creating and getting a note with only the required fields populated"""

        # Create labbook
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="notes-test-1", description="my first labbook10000")

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir[0]):
            # Make and validate request
            client = Client(fixture_working_dir[2])

            # Create a file in the LabBook and commit it
            working_dir = lb.git.config["working_directory"]
            labbook_dir = os.path.join(working_dir, "default", "default", "labbooks", "notes-test-1")
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
                   level: AUTO_MAJOR,
                   message: "Added a new file in this test",
                   linkedCommit: \"""" + str(commit) + """\",
                 })
                 {
                   note {
                     message              
                   }
                 }
               }
               """

            snapshot.assert_match(client.execute(query))

            query = """
               {
                   labbook(name: "notes-test-1", owner: "default") {
                       notes(first:1) {
                           edges {
                               node {                                                                                       
                                   message
                                   author
                                   level
                                   tags
                                   freeText
                                   objects {
                                       edges {
                                           node {
                                               key
                                               type
                                               value
                                           }
                                           cursor
                                       }
                                   }
                               }
                               cursor
                           }                        
                       }
                   }
               }
               """
            snapshot.assert_match(client.execute(query))

    def test_create_user_note(self, fixture_working_dir, snapshot):
        """Test creating and getting a user note"""

        # Create labbook
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="user-note-test", description="testing user notes")

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir[0]):
            # Make and validate request
            client = Client(fixture_working_dir[2])

            # Create a user note
            query = """
            mutation makeUserNote {
              createUserNote(input: {
                labbookName: "user-note-test",
                message: "I think this is a thing",
                freeText: "## A title\\n- sdf\\n - ghfg",
                tags: ["tag1", "tag2"],
                objects: [{key: "objectkey1", type: "PNG", value: "2new0x7FABC374FX"}]
              })
              {
                note {
                  message
                  freeText
                }
              }
            }
            """

            snapshot.assert_match(client.execute(query))

            query = """
            {
                labbook(name: "user-note-test", owner: "default") {
                    notes(first:1) {
                        edges {
                            node {
                                message
                                freeText
                                objects{
                                    edges{
                                        node{
                                            key
                                            type
                                            value
                                        }
                                    }
                                }
                                tags
                            }
                        }
                    }
                }
            }
            """
            snapshot.assert_match(client.execute(query))

    def test_create_user_note_no_details(self, fixture_working_dir, snapshot):
        """Test creating and getting a user note with no markdown body or tags"""

        # Create labbook
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="user-note-test", description="testing user notes")

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir[0]):
            # Make and validate request
            client = Client(fixture_working_dir[2])

            # Create a user note
            query = """
            mutation makeUserNote {
              createUserNote(input: {
                labbookName: "user-note-test",
                message: "I think this is a thing",
              })
              {
                note {
                  message
                  freeText
                }
              }
            }
            """

            snapshot.assert_match(client.execute(query))

            query = """
            {
                labbook(name: "user-note-test", owner: "default") {
                    notes(first:1) {
                        edges {
                            node {
                                message
                                freeText
                            }
                        }
                    }
                }
            }
            """
            snapshot.assert_match(client.execute(query))
