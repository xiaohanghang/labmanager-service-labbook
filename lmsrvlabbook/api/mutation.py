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
from lmsrvlabbook.api.mutations import CreateBranch, CheckoutBranch, CreateLabbook, BuildImage, StartContainer, \
    CreateNote, AddEnvironmentComponent, AddEnvironmentPackage, CreateUserNote, StopContainer


class LabbookMutations(graphene.AbstractType):
    """Entry point for all graphql mutations"""
    create_labbook = CreateLabbook.Field()
    create_branch = CreateBranch.Field()
    checkout_branch = CheckoutBranch.Field()
    build_image = BuildImage.Field()
    start_container = StartContainer.Field()
    stop_container = StopContainer.Field()
    create_note = CreateNote.Field()
    create_user_note = CreateUserNote.Field()
    add_environment_component = AddEnvironmentComponent.Field()
    add_environment_package = AddEnvironmentPackage.Field()
