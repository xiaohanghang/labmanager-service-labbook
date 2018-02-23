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
import flask
import redis
import os
import base64

from lmcommon.logging import LMLogger
from lmcommon.gitlib.git import GitAuthor
from lmsrvcore.auth.identity import get_identity_manager_instance
from lmcommon.auth.identity import User


def get_logged_in_user():
    """A method to get the current logged in User object"""
    # Check for user in redis cache
    access_token = flask.g.get('access_token', None)

    if access_token:
        # Build unique key from the bearer token
        key = access_token[0::6]

        # Get a redis client
        client = flask.g.get('redis_client', None)
        if not client:
            client = redis.StrictRedis(db=4)
            flask.g.redis_client = client

        # Check if user data is cached
        if client.exists(key):
            # Load user data from redis
            user = User()
            user.username = client.hget(key, "username").decode()
            user.email = client.hget(key, "email").decode()
            user.given_name = client.hget(key, "given_name").decode()
            user.family_name = client.hget(key, "family_name").decode()

        else:
            # User not loaded yet, so get it from the identity manager
            user = get_identity_manager_instance().get_user_profile(access_token)

            # Save to redis
            client.hset(key, "username", user.username)
            client.hset(key, "email", user.email)
            client.hset(key, "given_name", user.given_name)
            client.hset(key, "family_name", user.family_name)

            # Set a TTL of 5 minutes. This will auto-delete the key so the identity will be re-queried
            client.expire(key, 60 * 5)
    else:
        # No access token, so assume running locally or malformed request and force a full load from manager
        user = get_identity_manager_instance().get_user_profile(access_token)

    return user


def get_logged_in_username():
    """A Method to get the current logged in user's username


    Returns:
        str
    """
    user = get_logged_in_user()

    if not user:
        logger = LMLogger()
        logger.logger.error("Failed to load a user identity from request context.")
        raise ValueError("Failed to load a user identity from request context.")

    return user.username


def get_logged_in_author():
    """A Method to get the current logged in user's GitAuthor instance


    Returns:
        GitAuthor
    """
    user = get_logged_in_user()

    if not user:
        logger = LMLogger()
        logger.logger.error("Failed to load a user identity from request context.")
        raise ValueError("Failed to load a user identity from request context.")

    # Create a GitAuthor instance if possible

    return GitAuthor(name=user.username, email=user.email)
