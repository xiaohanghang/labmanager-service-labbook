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
    CreateNote, AddEnvironmentComponent, AddEnvironmentPackage, CreateUserNote, StopContainer, ImportLabbook, \
    ExportLabbook, MoveLabbookFile, DeleteLabbookFile, MakeLabbookDirectory


class LabbookMutations(graphene.AbstractType):
    """Entry point for all graphql mutations"""

    # Import a labbook from an uploaded file (Archive as zip).
    import_labbook = ImportLabbook.Field()

    # Export a labbook and return URL to its zipped archive.
    export_labbook = ExportLabbook.Field()

    # Create a new labbook on the file system.
    create_labbook = CreateLabbook.Field()

    # Create a new git branch for a given labbook.
    create_branch = CreateBranch.Field()

    # Update a given labbook to be at the tip of a particular git branch.
    checkout_branch = CheckoutBranch.Field()

    # Build a docker image for a given Labbook.
    build_image = BuildImage.Field()

    # Start a labbook's Docker container.
    start_container = StartContainer.Field()

    # Start a labbook's Docker container.
    stop_container = StopContainer.Field()

    # Create a note in the labbook's current working branch
    create_note = CreateNote.Field()

    # ???
    create_user_note = CreateUserNote.Field()

    # Add a development environment or complex dependency to Labbook environment.
    add_environment_component = AddEnvironmentComponent.Field()

    # Add a package to a Labbook environment (e.g., pip package, apt)
    add_environment_package = AddEnvironmentPackage.Field()

    # Move files or directory within a labbook
    move_labbook_file = MoveLabbookFile.Field()

    # Delete a file or directory inside of a Labbook.
    delete_labbook_file = DeleteLabbookFile.Field()

    # Make a directory (with auto-included .gitkeep) inside of a Labbook
    make_labbook_directory = MakeLabbookDirectory.Field()
