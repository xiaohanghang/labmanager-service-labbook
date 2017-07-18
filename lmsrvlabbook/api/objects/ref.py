
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
from lmcommon.labbook import LabBook

from lmsrvcore.auth.user import get_logged_in_user

from lmsrvcore.api.interfaces import GitRef

from lmsrvlabbook.api.objects import LabbookCommit


class LabbookRef(graphene.ObjectType):
    """An object representing a git reference in a LabBook repository"""
    class Meta:
        interfaces = (graphene.relay.Node, GitRef)

    # The target commit the reference points to
    commit = graphene.Field(LabbookCommit)

    @staticmethod
    def get_node(node_id, context, info):
        input_data = {"type_id": node_id}
        return LabbookRef.create(input_data)

    @staticmethod
    def to_type_id(id_data):
        """Method to generate a single string that uniquely identifies this object

        Args:
            id_data(dict):

        Returns:
            str
        """
        return "{}&{}&{}&{}".format(id_data["owner"], id_data["name"], id_data["prefix"], id_data["branch"])

    @staticmethod
    def parse_type_id(type_id):
        """Method to parse an ID for a given type into its identifiable variables returned as a dictionary of strings

        Args:
            type_id (str): type unique identifier

        Returns:
            dict
        """
        split = type_id.split("&")
        id_data = {"owner": split[0], "name": split[1], "branch": split[3]}
        if split[2] == "None":
            id_data["prefix"] = None
        else:
            id_data["prefix"] = split[2]

        return id_data

    @staticmethod
    def create(id_data):
        """Method to create a graphene LabbookRef object based on the type node ID or owner&name&prefix&branch

        id_data should at a minimum contain either `type_id` or `owner` & `name` & `hash`

            {
                "type_id": <unique id for this object Type),
                "username": <optional username for logged in user>,
                "owner": <owner username (or org)>,
                "name": <name of the labbook>
                "prefix": <branch prefix (e.g. 'origin', will be omitted null for local branches>
                "branch": <branch name>
                "git": <optional gitlib instance already instantiated>
            }

        Args:
            id_data(dict): A dictionary of variables that uniquely ID the instance

        Returns:
            LabbookCommit
        """
        if "username" not in id_data:
            # TODO: Lookup name based on logged in user when available
            id_data["username"] = get_logged_in_user()

        if "type_id" in id_data:
            # Parse ID components
            id_data.update(LabbookRef.parse_type_id(id_data["type_id"]))
            del id_data["type_id"]

        if "git" not in id_data:
            git = get_git_interface(Configuration().config["git"])
            git.set_working_directory(os.path.join(git.working_directory,
                                                   id_data["username"],
                                                   id_data["owner"],
                                                   id_data["name"]))
        else:
            git = id_data["git"]

        # Look up commit hash for a given ref
        git_path = id_data["branch"]
        if "prefix" in id_data:
            if id_data["prefix"]:
                git_path = "{}/{}".format(id_data["prefix"], id_data["branch"])
        else:
            id_data["prefix"] = None

        git_ref = git.repo.refs[git_path]
        id_data["hash"] = git_ref.commit.hexsha

        return LabbookRef(id=LabbookRef.to_type_id(id_data),
                          commit=LabbookCommit.create(id_data),
                          name=id_data["branch"], prefix=id_data["prefix"])
