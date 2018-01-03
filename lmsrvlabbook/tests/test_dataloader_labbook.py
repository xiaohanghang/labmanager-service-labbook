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
from datetime import datetime
from snapshottest import snapshot
from lmsrvlabbook.tests.fixtures import fixture_working_dir, fixture_working_dir_populated_scoped, fixture_test_file

from graphene.test import Client
import graphene
from mock import patch

from lmsrvlabbook.dataloader.labbook import LabBookLoader

from lmcommon.labbook import LabBook
from lmcommon.fixtures import remote_labbook_repo
from lmcommon.configuration import Configuration


def reject_method(err_msg):
    assert False, err_msg

d
class TestDataloaderLabBook(object):

    def test_load_one(self, fixture_working_dir):
        """Test loading 1 labbook"""

        def accept_method(lb):
            assert lb.name == "labbook1"
            assert lb.description == "my first labbook1"

        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook1", description="my first labbook1")
        lb.new(owner={"username": "default"}, name="labbook2", description="my first labbook2")
        lb.new(owner={"username": "test3"}, name="labbook2", description="my first labbook3")

        loader = LabBookLoader()

        key = f"default&default&labbook1"
        loader.load(key).then(accept_method, reject_method)

        # load again
        loader.load(key).then(accept_method, reject_method)

    def test_load_many(self, fixture_working_dir):
        """Test loading many labbooks"""

        def accept_method(lb):
            assert lb.name == "labbook1"
            assert lb.description == "my first labbook1"

        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook1", description="my first labbook1")
        lb.new(owner={"username": "default"}, name="labbook2", description="my first labbook2")
        lb.new(owner={"username": "test3"}, name="labbook2", description="my first labbook3")

        loader = LabBookLoader()

        keys = ["default&default&labbook1", "default&default&labbook2", "default&test3&labbook2dfdf"]
        loader.load_many(keys).then(accept_method, reject_method)

