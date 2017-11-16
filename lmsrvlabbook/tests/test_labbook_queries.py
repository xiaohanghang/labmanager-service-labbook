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
from lmsrvlabbook.tests.fixtures import fixture_working_dir, fixture_working_dir_populated_scoped

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


class TestLabBookServiceQueries(object):

    def test_list_labbooks(self, fixture_working_dir, snapshot):
        """Test listing labbooks"""

        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook1", description="my first labbook1")
        lb.new(owner={"username": "default"}, name="labbook2", description="my first labbook2")
        lb.new(owner={"username": "test3"}, name="labbook2", description="my first labbook3")

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir[0]):
            # Make and validate request
            client = Client(fixture_working_dir[2])

            # Get LabBooks for the "logged in user" - Currently just "default"
            query = """
            {
                localLabbooks {
                    edges {
                        node {
                            name
                            description
                        }
                        cursor
                    }
                }
            }
            """
            snapshot.assert_match(client.execute(query))

    def test_pagination_noargs(self, fixture_working_dir_populated_scoped, snapshot):
        # Mock the configuration class it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_populated_scoped[0]):
            client = Client(fixture_working_dir_populated_scoped[2])
            query = """
                    {
                        localLabbooks {
                            edges {
                                node {
                                    name
                                    description
                                }
                                cursor
                            }
                            pageInfo {
                                hasNextPage
                                hasPreviousPage
                            }
                        }
                    }
                    """
            snapshot.assert_match(client.execute(query))

    def test_pagination_first_only(self, fixture_working_dir_populated_scoped, snapshot):
        # Mock the configuration class it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_populated_scoped[0]):
            client = Client(fixture_working_dir_populated_scoped[2])
            query = """
                    {
                        localLabbooks(first: 3) {
                            edges {
                                node {
                                    name
                                    description
                                }
                                cursor
                            }
                            pageInfo {
                                hasNextPage
                                hasPreviousPage
                            }
                        }
                    }
                    """
            snapshot.assert_match(client.execute(query))

    def test_pagination_first_and_after(self, fixture_working_dir_populated_scoped, snapshot):
        # Nominal case
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_populated_scoped[0]):
            client = Client(fixture_working_dir_populated_scoped[2])
            query = """
                    {
                        localLabbooks(first: 4, after: "Mg==") {
                            edges {
                                node {
                                    name
                                    description
                                }
                                cursor
                            }
                            pageInfo {
                                hasNextPage
                                hasPreviousPage
                                startCursor
                                endCursor
                            }
                        }
                    }
                    """
            snapshot.assert_match(client.execute(query))

            # Overrunning end of list of labbooks
            query = """
                    {
                        localLabbooks(first: 6, after: "Ng==") {
                            edges {
                                node {
                                    name
                                    description
                                }
                                cursor
                            }
                            pageInfo {
                                hasNextPage
                                hasPreviousPage
                            }
                        }
                    }
                    """
            snapshot.assert_match(client.execute(query))

            # Overrunning end of list of labbooks, returns empty set.
            query = """
                    {
                        localLabbooks(first: 6, after: "OA==") {
                            edges {
                                node {
                                    name
                                    description
                                }
                                cursor
                            }
                            pageInfo {
                                hasNextPage
                                hasPreviousPage
                            }
                        }
                    }
                    """
            snapshot.assert_match(client.execute(query))

    def test_pagination_last_only(self, fixture_working_dir_populated_scoped, snapshot):

        # Mock the configuration class it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_populated_scoped[0]):
            client = Client(fixture_working_dir_populated_scoped[2])
            query = """
                    {
                        localLabbooks(last: 3) {
                            edges {
                                node {
                                    name
                                    description
                                }
                                cursor
                            }
                            pageInfo {
                                hasNextPage
                                hasPreviousPage
                            }
                        }
                    }
                    """
            snapshot.assert_match(client.execute(query))

    def test_pagination_last_and_before(self, fixture_working_dir_populated_scoped, snapshot):

        # Mock the configuration class it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_populated_scoped[0]):
            client = Client(fixture_working_dir_populated_scoped[2])
            query = """
                    {
                        localLabbooks(last: 3, before: "Nw==") {
                            edges {
                                node {
                                    name
                                    description
                                }
                                cursor
                            }
                            pageInfo {
                                hasNextPage
                                hasPreviousPage
                            }
                        }
                    }
                    """
            snapshot.assert_match(client.execute(query))

            # Overrun start of list
            query = """
                    {
                        localLabbooks(last: 3, before: "MQ==") {
                            edges {
                                node {
                                    name
                                    description
                                }
                                cursor
                            }
                            pageInfo {
                                hasNextPage
                                hasPreviousPage
                                startCursor
                                endCursor
                            }
                        }
                    }
                    """
            snapshot.assert_match(client.execute(query))

            # Overrun with no intersection (should return empty list)
            query = """
                    {
                        localLabbooks(last: 3, before: "MA==") {
                            edges {
                                node {
                                    name
                                    description
                                }
                                cursor
                            }
                            pageInfo {
                                hasNextPage
                                hasPreviousPage
                                startCursor
                                endCursor
                            }
                        }
                    }
                    """
            snapshot.assert_match(client.execute(query))

    def test_pagination(self, fixture_working_dir_populated_scoped, snapshot):
        """Test pagination and cursors"""

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_populated_scoped[0]):
            # Make and validate request
            client = Client(fixture_working_dir_populated_scoped[2])

            # Get LabBooks for the "logged in user" - Currently just "default"
            query = """
                    {
                        localLabbooks(first: 2, after: "MQ==") {
                            edges {
                                node {
                                    name
                                    description
                                }
                                cursor
                            }
                            pageInfo {
                                hasNextPage
                                hasPreviousPage
                            }
                        }
                    }
                    """
            snapshot.assert_match(client.execute(query))

            before_query = """
                    {
                        localLabbooks(last: 2, before: "Ng==") {
                            edges {
                                node {
                                    name
                                    description
                                }
                                cursor
                            }
                            pageInfo {
                                hasNextPage
                                hasPreviousPage
                            }
                        }
                    }
                    """
            snapshot.assert_match(client.execute(before_query))

    def test_get_labbook(self, fixture_working_dir, snapshot):
        """Test listing labbooks"""
        # Create labbooks
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook1", description="my first labbook1")

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir[0]):
            # Make and validate request
            client = Client(fixture_working_dir[2])

            # Get LabBooks for a single user - Don't get the ID field since it is a UUID
            query = """
            {
              labbook(name: "labbook1", owner: "default") {
                name
                description
                activeBranch {
                    name
                }
              }
            }
            """
            snapshot.assert_match(client.execute(query))

    def test_list_labbooks_container_status(self, fixture_working_dir, snapshot):
        """Test listing labbooks"""

        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook1", description="my first labbook1")
        lb.new(owner={"username": "default"}, name="labbook2", description="my first labbook2")
        lb.new(owner={"username": "test3"}, name="labbook2", description="my first labbook3")

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir[0]):
            # Make and validate request
            client = Client(fixture_working_dir[2])

            # Get LabBooks for the "logged in user" - Currently just "default"
            query = """
            {
                localLabbooks {
                    edges {
                        node {
                            name
                            description
                            environment{
                                imageStatus
                                containerStatus
                            }
                        }
                        cursor
                    }
                }
            }
            """
            snapshot.assert_match(client.execute(query))

    def test_list_labbooks_container_status_no_labbooks(self, fixture_working_dir, snapshot):
        """Test listing labbooks when none exist"""

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir[0]):
            # Make and validate request
            client = Client(fixture_working_dir[2])

            # Get LabBooks for the "logged in user" - Currently just "default"
            query = """
            {
                localLabbooks {
                    edges {
                        node {
                            name
                            description
                            environment{
                                imageStatus
                                containerStatus
                            }
                        }
                        cursor
                    }
                }
            }
            """
            snapshot.assert_match(client.execute(query))

    def test_walkdir(self, fixture_working_dir_populated_scoped, snapshot):
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir_populated_scoped[0]):
            # Make and validate request
            client = Client(fixture_working_dir_populated_scoped[2])
            query = """
            {
              labbook(name: "labbook1", owner: "default") {
                name
                files {
                    edges {
                        node {
                            id
                            key
                            modifiedAt
                            size
                            isDir
                        }
                    }
                }
              }
            }
            """
            result = client.execute(query)
            for n in result['data']['labbook']['files']['edges']:
                node = n['node']
                assert node['isDir'] is True
                assert node['modifiedAt'] is not None
                assert type(node['modifiedAt']) == int
                assert type(node['size']) == int
                assert node['key']

            query = """
                        {
                          labbook(name: "labbook1", owner: "default") {
                            name
                            files {
                                edges {
                                    node {
                                        id
                                        key
                                        size
                                        isDir
                                    }
                                }
                            }
                          }
                        }
                        """
            snapshot.assert_match(client.execute(query))

    def test_list_files_code(self, fixture_working_dir, snapshot):
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook1", description="my first labbook1")

        # Write data in code
        with open(os.path.join(lb.root_dir, 'code', "test_file1.txt"), 'wt') as tf:
            tf.write("file 1")
        with open(os.path.join(lb.root_dir, 'code', "test_file2.txt"), 'wt') as tf:
            tf.write("file 2!!!!!!!!!")
        with open(os.path.join(lb.root_dir, 'code', ".hidden_file.txt"), 'wt') as tf:
            tf.write("Should be hidden")

        # Create subdirs and data
        os.makedirs(os.path.join(lb.root_dir, 'code', 'src', 'js'))
        with open(os.path.join(lb.root_dir, 'code', 'src', 'test.py'), 'wt') as tf:
            tf.write("print('hello, world')")
        with open(os.path.join(lb.root_dir, 'code', 'src', 'js', 'test.js'), 'wt') as tf:
            tf.write("asdfasdf")

        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir[0]):
            # Make and validate request
            client = Client(fixture_working_dir[2])
            query = """
                        {
                          labbook(name: "labbook1", owner: "default") {
                            name
                            code{
                                files {
                                    edges {
                                        node {
                                            id
                                            key
                                            size
                                            isDir
                                        }
                                    }
                                }
                            }
                          }
                        }
                        """
            snapshot.assert_match(client.execute(query))

            # Just get the files in the sub-directory "js"
            query = """
                        {
                          labbook(name: "labbook1", owner: "default") {
                            name
                            code{
                                files(root: "src") {
                                    edges {
                                        node {
                                            id
                                            key
                                            size
                                            isDir
                                        }
                                    }
                                }
                            }
                          }
                        }
                        """
            snapshot.assert_match(client.execute(query))

            # Just get the files in the sub-directory "js"
            query = """
                        {
                          labbook(name: "labbook1", owner: "default") {
                            name
                            code{
                                files(root: "src/") {
                                    edges {
                                        node {
                                            id
                                            key
                                            size
                                            isDir
                                        }
                                    }
                                }
                            }
                          }
                        }
                        """
            snapshot.assert_match(client.execute(query))

    def test_list_files_many(self, fixture_working_dir, snapshot):
        # Add some extra files for listing
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook1", description="my first labbook1")

        # Write data in code
        with open(os.path.join(lb.root_dir, 'code', "test_file1.txt"), 'wt') as tf:
            tf.write("file 1")
        with open(os.path.join(lb.root_dir, 'code', "test_file2.txt"), 'wt') as tf:
            tf.write("file 2!!!!!!!!!")
        with open(os.path.join(lb.root_dir, 'code', ".hidden_file.txt"), 'wt') as tf:
            tf.write("Should be hidden")

        # Create subdirs and data
        os.makedirs(os.path.join(lb.root_dir, 'input', 'subdir', 'data'))
        os.makedirs(os.path.join(lb.root_dir, 'output', 'empty'))
        with open(os.path.join(lb.root_dir, 'input', 'subdir', 'data.dat'), 'wt') as tf:
            tf.write("adsfasdfasdf")
        with open(os.path.join(lb.root_dir, 'output', 'result.dat'), 'wt') as tf:
            tf.write("fgh")

        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir[0]):
            # Make and validate request
            client = Client(fixture_working_dir[2])
            query = """
                        {
                          labbook(name: "labbook1", owner: "default") {
                            name
                            code{
                                files {
                                    edges {
                                        node {
                                            id
                                            key
                                            size
                                            isDir
                                        }
                                    }
                                }
                            }
                            input{
                                files {
                                    edges {
                                        node {
                                            id
                                            key
                                            size
                                            isDir
                                        }
                                    }
                                }
                            }
                            output{
                                files {
                                    edges {
                                        node {
                                            id
                                            key
                                            size
                                            isDir
                                        }
                                    }
                                }
                            }
                          }
                        }
                        """
            snapshot.assert_match(client.execute(query))

            # Just get the files in the sub-directory "js"
            query = """
                    {
                      labbook(name: "labbook1", owner: "default") {
                        name
                        code{
                            files {
                                edges {
                                    node {
                                        id
                                        key
                                        size
                                        isDir
                                    }
                                }
                            }
                        }
                        input{
                            files(root: "subdir") {
                                edges {
                                    node {
                                        id
                                        key
                                        size
                                        isDir
                                    }
                                }
                            }
                        }
                        output{
                            files(root: "empty") {
                                edges {
                                    node {
                                        id
                                        key
                                        size
                                        isDir
                                    }
                                }
                            }
                        }
                      }
                    }
                    """
            snapshot.assert_match(client.execute(query))

    def test_list_favorites(self, fixture_working_dir, snapshot):
        """Test listing labbook favorites"""

        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook1", description="my first labbook1")

        # Setup some favorites in code
        with open(os.path.join(lb.root_dir, 'code', 'test1.txt'), 'wt') as test_file:
            test_file.write("blah1")
        with open(os.path.join(lb.root_dir, 'code', 'test2.txt'), 'wt') as test_file:
            test_file.write("blah2")

        # Setup a favorite dir in input
        os.makedirs(os.path.join(lb.root_dir, 'code', 'blah'))
        os.makedirs(os.path.join(lb.root_dir, 'input', 'data1'))
        os.makedirs(os.path.join(lb.root_dir, 'output', 'data2'))

        # Create favorites
        lb.create_favorite("code", "test1.txt", description="My file with stuff 1")
        lb.create_favorite("code", "test2.txt", description="My file with stuff 2")
        lb.create_favorite("code", "blah/", description="testing", is_dir=True)
        lb.create_favorite("input", "data1/", description="Data dir 1", is_dir=True)
        lb.create_favorite("output", "data2/", description="Data dir 2", is_dir=True)

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir[0]):
            # Make and validate request
            client = Client(fixture_working_dir[2])

            # Get LabBooks for the "logged in user" - Currently just "default"
            query = """
                        {
                          labbook(name: "labbook1", owner: "default") {
                            name
                            code{
                                favorites{
                                    edges {
                                        node {
                                            id
                                            index
                                            key
                                            description
                                            isDir
                                        }
                                    }
                                }
                            }
                          }
                        }
                        """
            snapshot.assert_match(client.execute(query))

            # Get input favorites
            query = """
                        {
                          labbook(name: "labbook1", owner: "default") {
                            name
                            input{
                                favorites{
                                    edges {
                                        node {
                                            id
                                            index
                                            key
                                            description
                                            isDir
                                        }
                                    }
                                }
                            }
                          }
                        }
                        """
            snapshot.assert_match(client.execute(query))

            # Get output favorites
            query = """
                        {
                          labbook(name: "labbook1", owner: "default") {
                            name
                            output{
                                favorites{
                                    edges {
                                        node {
                                            id
                                            index
                                            key
                                            description
                                            isDir
                                        }
                                    }
                                }
                            }
                          }
                        }
                        """
            snapshot.assert_match(client.execute(query))

            # Get all favorites
            query = """
                        {
                          labbook(name: "labbook1", owner: "default") {
                            name
                            code{
                                favorites{
                                    edges {
                                        node {
                                            id
                                            index
                                            key
                                            description
                                            isDir
                                        }
                                    }
                                }
                            }
                            input{
                                favorites{
                                    edges {
                                        node {
                                            id
                                            index
                                            key
                                            description
                                            isDir
                                        }
                                    }
                                }
                            }
                            output{
                                favorites{
                                    edges {
                                        node {
                                            id
                                            index
                                            key
                                            description
                                            isDir
                                        }
                                    }
                                }
                            }
                          }
                        }
                        """
            snapshot.assert_match(client.execute(query))

    def test_list_favorite_and_files(self, fixture_working_dir, snapshot):
        """Test listing labbook favorites"""
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook1", description="my first labbook1")

        # Setup some favorites in code
        with open(os.path.join(lb.root_dir, 'code', 'test1.txt'), 'wt') as test_file:
            test_file.write("blah1")
        with open(os.path.join(lb.root_dir, 'code', 'test2.txt'), 'wt') as test_file:
            test_file.write("blah2")

        # Setup a favorite dir in input
        os.makedirs(os.path.join(lb.root_dir, 'code', 'blah'))

        # Create favorites
        lb.create_favorite("code", "test2.txt", description="My file with stuff 2")
        lb.create_favorite("code", "blah/", description="testing", is_dir=True)

        # Mock the configuration class it it returns the same mocked config file
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir[0]):
            # Make and validate request
            client = Client(fixture_working_dir[2])

            # Get LabBooks for the "logged in user" - Currently just "default"
            query = """
                        {
                          labbook(name: "labbook1", owner: "default") {
                            name
                            code{
                                favorites{
                                    edges {
                                        node {
                                            id
                                            index
                                            key
                                            description
                                            isDir
                                        }
                                    }
                                }                                
                                files {
                                    edges {
                                        node {
                                            id
                                            key
                                            size
                                            isDir
                                        }
                                    }
                                }
                            }
                          }
                        }
                        """
            snapshot.assert_match(client.execute(query))

    def test_list_all_files_many(self, fixture_working_dir, snapshot):
        # Add some extra files for listing
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook1", description="my first labbook1")

        # Write data in code
        with open(os.path.join(lb.root_dir, 'code', "test_file1.txt"), 'wt') as tf:
            tf.write("file 1")
        with open(os.path.join(lb.root_dir, 'code', "test_file2.txt"), 'wt') as tf:
            tf.write("file 2!!!!!!!!!")
        with open(os.path.join(lb.root_dir, 'code', ".hidden_file.txt"), 'wt') as tf:
            tf.write("Should be hidden")

        # Create subdirs and data
        os.makedirs(os.path.join(lb.root_dir, 'input', 'subdir', 'data'))
        os.makedirs(os.path.join(lb.root_dir, 'output', 'empty'))
        with open(os.path.join(lb.root_dir, 'input', 'subdir', 'data.dat'), 'wt') as tf:
            tf.write("adsfasdfasdf")
        with open(os.path.join(lb.root_dir, 'output', 'result.dat'), 'wt') as tf:
            tf.write("fgh")

        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir[0]):
            # Make and validate request
            client = Client(fixture_working_dir[2])
            query = """
                        {
                          labbook(name: "labbook1", owner: "default") {
                            name
                            code{
                                allFiles {
                                    edges {
                                        node {
                                            id
                                            key
                                            size
                                            isDir
                                        }
                                    }
                                }
                            }
                            input{
                                allFiles {
                                    edges {
                                        node {
                                            id
                                            key
                                            size
                                            isDir
                                        }
                                    }
                                }
                            }
                            output{
                                allFiles {
                                    edges {
                                        node {
                                            id
                                            key
                                            size
                                            isDir
                                        }
                                    }
                                }
                            }
                          }
                        }
                        """
            snapshot.assert_match(client.execute(query))
