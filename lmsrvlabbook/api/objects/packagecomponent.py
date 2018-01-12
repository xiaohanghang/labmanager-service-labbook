
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


class PackageComponent(graphene.ObjectType, interfaces=(graphene.relay.Node,)):
    """A type that represents a Package Manager based Environment Component"""
    # The loaded yaml data
    _component_data = None

    # The name of the package manager
    manager = graphene.String(required=True)

    # The name of the package
    package = graphene.String(required=True)

    # The current version of the package
    version = graphene.String(required=True)

    # The latest available version of the package
    latest_version = graphene.String()

    # Flag indicating if the component is in the Base
    from_base = graphene.Boolean()

    @classmethod
    def get_node(cls, info, id):
        """Method to resolve the object based on it's Node ID"""
        # Parse the key
        manager, package, version = id.split("&")

        return PackageComponent(id=f"{manager}&{package}&{version}",
                                manager=manager, package=package, version=version)

    def resolve_id(self, info):
        """Resolve the unique Node id for this object"""
        if not self.manager or not self.package or self.version is None:
            raise ValueError("Resolving a PackageComponent ID requires manager, package and version to be set")

        return f"{self.manager}&{self.package}&{self.version}"

    def resolve_latest_version(self, info):
        """Resolve the latest_version field"""
        raise NotImplemented

    def resolve_from_base(self, info):
        """Resolve the from_base field"""
        if self.from_base is None:
            # Assume not from base if value is not set on construction
            return False
        else:
            return self.from_base

