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
from flask import current_app

from lmcommon.configuration import Configuration


class TestUserIdentityQueries(object):

    def test_logged_in_user(self, fixture_working_dir, snapshot):
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir[0]):
            # Make and validate request
            client = Client(fixture_working_dir[2])

            query = """
                    {
                        userIdentity{
                                      id
                                      username
                                      email
                                      givenName
                                      familyName
                                    }
                    }
                    """

            snapshot.assert_match(client.execute(query))

    def test_no_logged_in_user(self, fixture_working_dir, snapshot):
        with patch.object(Configuration, 'find_default_config', lambda self: fixture_working_dir[0]):
            # Make and validate request
            client = Client(fixture_working_dir[2])

            query = """
                    {
                        userIdentity{
                                      id
                                      username
                                      email
                                      givenName
                                      familyName
                                    }
                    }
                    """

            # Delete the stored user context
            current_app.current_user = None
            user_dir = os.path.join(fixture_working_dir[1], '.labmanager', 'identity')
            os.remove(os.path.join(user_dir, 'user.json'))

            # Run query
            snapshot.assert_match(client.execute(query))