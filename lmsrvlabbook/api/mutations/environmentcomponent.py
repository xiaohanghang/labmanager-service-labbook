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

from lmcommon.logging import LMLogger
from lmcommon.labbook import LabBook
from lmcommon.environment import ComponentManager
from lmsrvcore.auth.user import get_logged_in_username

from lmsrvlabbook.api.objects.environmentcomponentid import EnvironmentComponentClass, EnvironmentComponent
from lmsrvlabbook.api.objects.packagemanager import PackageManager

logger = LMLogger.get_logger()


class AddEnvironmentPackage(graphene.relay.ClientIDMutation):
    """Mutation to add a new package to labbook. """

    class Input:
        labbook_name = graphene.String(required=True)
        owner = graphene.String()
        package_manager = graphene.String(required=True)
        package_name = graphene.String(required=True)
        package_version = graphene.String()

    environment_package = graphene.Field(lambda: PackageManager)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        # TODO: Lookup name based on logged in user when available
        username = get_logged_in_username()

        if not input.get("owner"):
            owner = username
        else:
            owner = input.get("owner")

        # Load LabBook instance
        lb = LabBook()
        lb.from_name(username, owner, input.get('labbook_name'))

        # Create Component Manager
        cm = ComponentManager(lb)
        cm.add_package(package_manager=input.get('package_manager'),
                       package_name=input.get('package_name'),
                       package_version=input.get('package_version'))

        id_data = {
            'component_class': 'package_manager',
            'package_manager': input.get('package_manager'),
            'package_name': input.get('package_name'),
            'package_version': input.get('package_version')
        }
        try:
            pkg_mgr = PackageManager.create(id_data)
        except Exception as e:
            logger.exception(e)
            raise

        return AddEnvironmentPackage(environment_package=pkg_mgr)


class AddEnvironmentComponent(graphene.relay.ClientIDMutation):
    """Mutation to add a new environment component to a LabBook"""

    class Input:
        labbook_name = graphene.String(required=True)
        owner = graphene.String()
        component_class = graphene.Field(EnvironmentComponentClass, required=True)
        repository = graphene.String(required=True)
        namespace = graphene.String(required=True)
        component = graphene.String(required=True)
        version = graphene.String(required=True)

    # TODO: Return updated LabBook Environment Component Collection
    environment_component = graphene.Field(lambda: EnvironmentComponent)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        # TODO: Lookup name based on logged in user when available
        username = get_logged_in_username()

        if not input.get("owner"):
            owner = username
        else:
            owner = input.get("owner")

        # Load LabBook instance
        lb = LabBook()
        lb.from_name(username, owner, input.get('labbook_name'))

        # Create Component Manager
        cm = ComponentManager(lb)
        cm.add_component(EnvironmentComponentClass.get(input.get('component_class')).name,
                         input.get('repository'),
                         input.get('namespace'),
                         input.get('component'),
                         input.get('version'))

        id_data = {
            'component_class': EnvironmentComponentClass.get(input.get('component_class')).name,
            'repo': input.get('repository'),
            'namespace': input.get('namespace'),
            'component': input.get('component'),
            'version': input.get('version')
        }
        try:
            env_component = EnvironmentComponent.create(id_data)
        except Exception as e:
            logger.exception(e)
            raise

        return AddEnvironmentComponent(environment_component=env_component)
