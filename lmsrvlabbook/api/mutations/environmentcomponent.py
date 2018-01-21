# Copyright (c) 2018 FlashX, LLC
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

from lmcommon.logging import LMLogger
from lmcommon.labbook import LabBook
from lmcommon.environment import ComponentManager

from lmsrvcore.auth.user import get_logged_in_username

from lmsrvlabbook.api.objects.packagecomponent import PackageComponent
from lmsrvlabbook.api.objects.customcomponent import CustomComponent
from lmsrvlabbook.api.connections.environment import CustomComponentConnection, PackageComponentConnection


class AddPackageComponent(graphene.relay.ClientIDMutation):
    """Mutation to add a new package to labbook"""

    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        manager = graphene.String(required=True)
        package = graphene.String(required=True)
        version = graphene.String()

    new_package_component_edge = graphene.Field(lambda: PackageComponentConnection.Edge)

    @classmethod
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, manager, package, version=None,
                               client_mutation_id=None):
        username = get_logged_in_username()

        # Load LabBook instance
        lb = LabBook()
        lb.from_name(username, owner, labbook_name)

        if version is None:
            # TODO: Use package manager instance to get the latest version if not specified
            version = "1.0"

        # Create Component Manager
        cm = ComponentManager(lb)
        cm.add_package(package_manager=manager,
                       package_name=package,
                       package_version=version,
                       from_base=False)

        # TODO: get cursor by checking how many packages are already installed

        new_edge = PackageComponentConnection.Edge(node=PackageComponent(manager=manager, package=package,
                                                                         version=version),
                                                   cursor=0)

        return AddPackageComponent(new_package_component_edge=new_edge)


class RemovePackageComponent(graphene.relay.ClientIDMutation):
    """Mutation to remove a package from labbook"""

    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        manager = graphene.String(required=True)
        package = graphene.String(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, manager, package,
                               client_mutation_id=None):
        username = get_logged_in_username()

        # Load LabBook instance
        lb = LabBook()
        lb.from_name(username, owner, labbook_name)

        # Create Component Manager
        cm = ComponentManager(lb)
        cm.remove_package(package_manager=manager, package_name=package)

        return RemovePackageComponent(success=True)


class AddCustomComponent(graphene.relay.ClientIDMutation):
    """Mutation to add a new environment component to a LabBook"""

    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        repository = graphene.String(required=True)
        component_id = graphene.String(required=True)
        revision = graphene.Int(required=True)

    new_custom_component_edge = graphene.Field(lambda: CustomComponentConnection.Edge)

    @classmethod
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, repository, component_id, revision,
                               client_mutation_id=None):
        username = get_logged_in_username()

        # Load LabBook instance
        lb = LabBook()
        lb.from_name(username, owner, labbook_name)

        # Create Component Manager
        cm = ComponentManager(lb)
        cm.add_component("custom", repository, component_id, revision)

        # TODO: get cursor by checking how many packages are already installed

        new_edge = CustomComponentConnection.Edge(node=CustomComponent(repository=repository, component_id=component_id,
                                                                       revision=revision),
                                                  cursor=0)

        return AddCustomComponent(new_custom_component_edge=new_edge)


class RemoveCustomComponent(graphene.relay.ClientIDMutation):
    """Mutation to remove an environment component to a LabBook"""

    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        repository = graphene.String(required=True)
        component_id = graphene.String(required=True)
        revision = graphene.Int(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, repository, component_id, revision,
                               client_mutation_id=None):
        username = get_logged_in_username()

        # Load LabBook instance
        lb = LabBook()
        lb.from_name(username, owner, labbook_name)

        # Create Component Manager
        cm = ComponentManager(lb)
        cm.remove_component("custom", repository, component_id, revision)

        return RemoveCustomComponent(success=True)
