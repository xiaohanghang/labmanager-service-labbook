
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
import os

from lmcommon.gitlib import get_git_interface
from lmcommon.configuration import Configuration

from lmsrvcore.auth.user import get_logged_in_username

from lmsrvcore.api import ObjectType
from lmsrvcore.api.interfaces import GitCommit


class LabbookCommit(ObjectType):
    """An object representing a commit to a LabBook"""
    class Meta:
        interfaces = (GitCommit, graphene.relay.Node)

    @staticmethod
    def to_type_id(id_data):
        """Method to generate a single string that uniquely identifies this object

        Args:
            id_data(dict):

        Returns:
            str
        """
        return "{}&{}&{}".format(id_data["owner"], id_data["name"], id_data["hash"])

    @staticmethod
    def parse_type_id(type_id):
        """Method to parse an ID for a given type into its identifiable variables returned as a dictionary of strings

        Args:
            type_id (str): type unique identifier

        Returns:
            dict
        """
        split = type_id.split("&")
        return {"owner": split[0], "name": split[1], "hash": split[2]}

    @staticmethod
    def create(id_data):
        """Method to create a graphene LabBookCommit object based on the type node ID or owner+name+hash

        id_data should at a minimum contain either `type_id` or `owner` & `name` & `hash`

            {
                "type_id": <unique id for this object Type),
                "username": <optional username for logged in user>,
                "owner": <owner username (or org)>,
                "name": <name of the labbook>,
                "hash": <full hexsha hash of the commit>,
                "git": <optional gitlib instance already instantiated>
            }

        Args:
            id_data(dict): A dictionary of variables that uniquely ID the instance

        Returns:
            LabbookCommit
        """
        if "username" not in id_data:
            id_data["username"] = get_logged_in_username()

        if "type_id" in id_data:
            # Parse ID components
            id_data.update(LabbookCommit.parse_type_id(id_data["type_id"]))
            del id_data["type_id"]

        # Get the commit information
        if "git" not in id_data:
            git = get_git_interface(Configuration().config["git"])
            git.set_working_directory(os.path.join(git.working_directory,
                                                   id_data["username"],
                                                   id_data["owner"],
                                                   "labbooks",
                                                   id_data["name"]))
        else:
            git = id_data["git"]

        committed_on = git.repo.commit(id_data["hash"]).committed_datetime.isoformat()

        return LabbookCommit(id=LabbookCommit.to_type_id(id_data),
                             hash=id_data["hash"], short_hash=id_data["hash"][:8],
                             committed_on=committed_on)
