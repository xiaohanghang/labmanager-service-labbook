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
import graphene
from lmsrvcore.api.interfaces import User
from lmsrvcore.api import ObjectType

from flask import current_app


class UserIdentity(ObjectType, interfaces=(graphene.relay.Node, User)):
    """A type representing the identity of the logged in user"""

    @staticmethod
    def to_type_id(dummy):
        """Method to generate a single string that uniquely identifies this object

        Args:
            dummy(str): A dummy far since this Object doesn't actually use type ids because users a loaded based on
                        authentication

        Returns:
            str
        """
        raise ValueError("UserIdentity type is set explicitly to the logged-in user. Do not call this method.")

    @staticmethod
    def parse_type_id(type_id):
        """Method to parse an ID for a given type into its identifiable variables returned as a dictionary of strings

        Args:
            type_id (str): type unique identifier

        Returns:
            dict
        """
        return type_id

    @staticmethod
    def create(dummy):
        """Method to populate a complete ObjectType instance from a dictionary that uniquely identifies an instances

        Args:
            dummy(str): A dummy far since this Object doesn't actually use type ids because users a loaded based on
                        authentication

        Returns:
            UserIdentity
        """
        # Get the user from the current flask context
        try:
            user = current_app.current_user
        except AttributeError:
            user = None

        if user:
            return UserIdentity(id=user.username,
                                username=user.username,
                                email=user.email,
                                given_name=user.given_name,
                                family_name=user.family_name)
        else:
            return None

