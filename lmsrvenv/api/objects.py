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


class ImageStatus(graphene.Enum):
    """An enumeration for Docker image status"""
    # The image has not be built locally yet
    DOES_NOT_EXIST = 0
    # The image is being built
    BUILD_IN_PROGRESS = 1
    # The image has been built and the Dockerfile has yet to change
    EXISTS = 2
    # The image has been built and the Dockerfile has been edited
    STALE = 3


class ContainerStatus(graphene.Enum):
    """An enumeration for container image status"""
    # The container is not running
    NOT_RUNNING = 0
    # The container is starting
    STARTING = 1
    # The container is running
    RUNNING = 2


class Environment(graphene.ObjectType):
    """A type that represents the Environment for a LabBook"""
    # The name of the current branch
    image_status = graphene.Field(ImageStatus)

    # The name of the current branch
    container_status = graphene.Field(ContainerStatus)

