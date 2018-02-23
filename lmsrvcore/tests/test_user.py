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
import flask
import redis

from lmsrvcore.auth.user import get_logged_in_author, get_logged_in_username, get_logged_in_user
from lmcommon.gitlib.git import GitAuthor
from lmsrvcore.tests.fixtures import fixture_working_dir_with_cached_user


class TestUserAuthHelpers(object):
    def test_get_logged_in_user(self, fixture_working_dir_with_cached_user):
        """Test getting identity manager in a flask app"""

        user = get_logged_in_user()
        assert user.username == "default"
        assert user.email == "jane@doe.com"
        assert user.given_name == "Jane"
        assert user.family_name == "Doe"

    def test_get_logged_in_user_cached(self, fixture_working_dir_with_cached_user):
        """Test getting identity manager in a flask app"""
        # Fake a token
        flask.g.access_token = "asioauhsdfikollhasdfioluasdlkfbjxclmjvkbdwklurfghaisudfhbasilkdfbaiwulsfbklsadbvf"

        user = get_logged_in_user()
        assert user.username == "default"
        assert user.email == "jane@doe.com"
        assert user.given_name == "Jane"
        assert user.family_name == "Doe"

        # User should now be loaded into redis
        client = redis.StrictRedis(db=4)
        key = flask.g.access_token[0::6]
        assert "default" == client.hget(key, "username").decode()
        assert "jane@doe.com" == client.hget(key, "email").decode()
        assert "Jane" == client.hget(key, "given_name").decode()
        assert "Doe" == client.hget(key, "family_name").decode()

    def test_get_logged_in_username(self, fixture_working_dir_with_cached_user):
        """Test authorization middlewhere when loading a user exists locally"""
        assert get_logged_in_username() == "default"

    def test_get_logged_in_author(self, fixture_working_dir_with_cached_user):
        """Test authorization middlewhere when a token header is malformed"""

        author = get_logged_in_author()
        assert type(author) == GitAuthor
        assert author.name == "default"
        assert author.email == "jane@doe.com"
