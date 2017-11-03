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
import base64
import os
from docker.errors import ImageNotFound

import graphene

from lmcommon.configuration import Configuration, get_docker_client
from lmcommon.dispatcher import (Dispatcher, jobs)
from lmcommon.labbook import LabBook
from lmcommon.logging import LMLogger
from lmcommon.notes import NoteStore, NoteLogLevel
from lmcommon.imagebuilder import ImageBuilder

from lmsrvcore.api.mutations import ChunkUploadMutation, ChunkUploadInput
from lmsrvcore.auth.user import get_logged_in_username
from lmsrvlabbook.api.connections.labbookfileconnection import LabbookFavoriteConnection
from lmsrvlabbook.api.connections.labbookfileconnection import LabbookFileConnection
from lmsrvlabbook.api.objects.labbook import Labbook
from lmsrvlabbook.api.objects.labbookfile import LabbookFavorite, LabbookFile

logger = LMLogger.get_logger()


class CreateLabbook(graphene.relay.ClientIDMutation):
    """Mutator for creation of a new Labbook on disk"""

    class Input:
        name = graphene.String(required=True)
        description = graphene.String(required=True)

    # Return the LabBook instance
    labbook = graphene.Field(lambda: Labbook)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        username = get_logged_in_username()

        # Create a new empty LabBook
        lb = LabBook()
        # TODO: Set owner/namespace properly once supported fully
        lb.new(owner={"username": username},
               username=username,
               name=input.get('name'),
               description=input.get('description'))

        # Create a new Note entry
        ns = NoteStore(lb)
        note_data = {
            "linked_commit": lb.git.commit_hash,
            "message": "Created new LabBook: {}/{}".format(username, input.get('name')),
            "level": NoteLogLevel.USER_MAJOR,
            "tags": [],
            "free_text": "",
            "objects": []
        }

        ns.create_note(note_data)

        # Get a graphene instance of the newly created LabBook
        id_data = {"owner": username,
                   "name": lb.name,
                   "username": username}
        new_labbook = Labbook.create(id_data)
        return CreateLabbook(labbook=new_labbook)


class RenameLabbook(graphene.ClientIDMutation):
    """Rename a labbook"""
    class Input:
        user = graphene.String(required=True)
        owner = graphene.String(required=True)
        original_labbook_name = graphene.String(required=True)
        new_labbook_name = graphene.String(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        try:
            # Load LabBook
            username = get_logged_in_username()

            working_directory = Configuration().config['git']['working_directory']
            inferred_lb_directory = os.path.join(working_directory, username, input['owner'], 'labbooks',
                                                 input['original_labbook_name'])
            lb = LabBook()
            lb.from_directory(inferred_lb_directory)

            # Image names
            old_tag = '{}-{}-{}'.format(username, input['owner'], input.get('original_labbook_name'))
            new_tag = '{}-{}-{}'.format(username, input['owner'], input.get('new_labbook_name'))

            # Rename LabBook
            lb.rename(input['new_labbook_name'])
            logger.info(f"Renamed LabBook from `{input['original_labbook_name']}` to `{input['new_labbook_name']}`")

            # Build image with new name...should be fast and use the Docker cache
            client = get_docker_client()
            image_builder = ImageBuilder(lb.root_dir)
            image_builder.build_image(docker_client=client, image_tag=new_tag, username=username, background=True)

            # Delete old image if it had previously been built successfully
            try:
                client.images.get(old_tag)
                client.images.remove(old_tag)
            except ImageNotFound:
                logger.warning(f"During renaming, original image {old_tag} not found, removal skipped.")

        except Exception as e:
            logger.exception(e)
            raise

        return RenameLabbook(success=True)


class ExportLabbook(graphene.relay.ClientIDMutation):
    class Input:
        user = graphene.String(required=True)
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)

    job_key = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        logger.info(f'Exporting LabBook: {input["user"]}/{input["owner"]}/{input["labbook_name"]}')
        try:
            working_directory = Configuration().config['git']['working_directory']
            inferred_lb_directory = os.path.join(working_directory, input['user'], input['owner'], 'labbooks',
                                                 input['labbook_name'])
            lb = LabBook()
            lb.from_directory(inferred_lb_directory)

            job_metadata = {'method': 'export_labbook_as_zip', 'labbook': lb.root_dir}
            job_kwargs = {'labbook_path': lb.root_dir, 'lb_export_directory': os.path.join(working_directory, 'export')}
            dispatcher = Dispatcher()
            job_key = dispatcher.dispatch_task(jobs.export_labbook_as_zip, kwargs=job_kwargs, metadata=job_metadata)
            logger.info(f"Exporting LabBook {lb.root_dir} in background job with key {job_key.key_str}")
        except Exception as e:
            logger.exception(e)
            raise
        return ExportLabbook(job_key=job_key.key_str)


class ImportLabbook(graphene.relay.ClientIDMutation, ChunkUploadMutation):
    class Input:
        owner = graphene.String(required=True)
        user = graphene.String(required=True)
        chunk_upload_params = ChunkUploadInput(required=True)

    import_job_key = graphene.String()
    build_image_job_key = graphene.String()

    @classmethod
    def mutate_and_process_upload(cls, input, context, info):
        if not cls.upload_file_path:
            logger.error('No file uploaded')
            raise ValueError('No file uploaded')

        logger.info(
            f"Handling ImportLabbook mutation: user={input.get('user')},"
            f"owner={input.get('owner')}. Uploaded file {cls.upload_file_path}")

        job_metadata = {'method': 'import_labbook_from_zip'}
        job_kwargs = {
            'archive_path': cls.upload_file_path,
            'username': input.get('user'),
            'owner': input.get('owner'),
            'base_filename': cls.filename
        }
        dispatcher = Dispatcher()
        job_key = dispatcher.dispatch_task(jobs.import_labboook_from_zip, kwargs=job_kwargs, metadata=job_metadata)
        logger.info(f"Importing LabBook {cls.upload_file_path} in background job with key {job_key.key_str}")

        assumed_lb_name = cls.filename.replace('.lbk', '').split('_')[0]
        working_directory = Configuration().config['git']['working_directory']
        inferred_lb_directory = os.path.join(working_directory, input['user'], input['owner'], 'labbooks',
                                             assumed_lb_name)
        build_img_kwargs = {
            'path': os.path.join(inferred_lb_directory, '.gigantum', 'env'),
            'tag': f"{input.get('user')}-{input.get('owner')}-{assumed_lb_name}",
            'pull': True,
            'nocache': False
        }
        build_img_metadata = {
            'method': 'build_image',
            'labbook': f"{input.get('user')}-{input.get('owner')}-{assumed_lb_name}"
        }
        logger.info(f"Queueing job to build imported labbook at assumed directory `{inferred_lb_directory}`")
        build_image_job_key = dispatcher.dispatch_task(jobs.build_docker_image, kwargs=build_img_kwargs,
                                                       dependent_job=job_key, metadata=build_img_metadata)
        logger.info(f"Adding dependent job {build_image_job_key} to build "
                    f"Docker image for labbook `{inferred_lb_directory}`")

        return ImportLabbook(import_job_key=job_key.key_str, build_image_job_key=build_image_job_key.key_str)


class AddLabbookFile(graphene.relay.ClientIDMutation, ChunkUploadMutation):
    """Mutation to add a file to a labbook. File should be sent in the `uploadFile` key as a multi-part/form upload.
    file_path is the relative path from the labbook root."""
    class Input:
        user = graphene.String(required=True)
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        file_path = graphene.String(required=True)
        chunk_upload_params = ChunkUploadInput(required=True)

    new_labbook_file_edge = graphene.Field(LabbookFileConnection.Edge)

    @classmethod
    def mutate_and_process_upload(cls, input, context, info):
        if not cls.upload_file_path:
            logger.error('No file uploaded')
            raise ValueError('No file uploaded')

        try:
            username = get_logged_in_username()

            working_directory = Configuration().config['git']['working_directory']
            inferred_lb_directory = os.path.join(working_directory, username, input['owner'], 'labbooks',
                                                 input['labbook_name'])
            lb = LabBook()
            lb.from_directory(inferred_lb_directory)

            # Insert into labbook
            file_info = lb.insert_file(src_file=cls.upload_file_path, dst_dir=os.path.dirname(input['file_path']),
                                       base_filename=cls.filename)

            logger.debug(f"Removing copied temp file {cls.upload_file_path}")
            os.remove(cls.upload_file_path)

            # Create data to populate edge
            id_data = {'username': username,
                       'owner': input.get('owner'),
                       'name': input.get('labbook_name'),
                       'file_info': file_info}

            # TODO: Fix cursor implementation, this currently doesn't make sense when adding edges
            cursor = base64.b64encode(f"{0}".encode('utf-8'))

        except Exception as e:
            logger.exception(e)
            raise

        return AddLabbookFile(new_labbook_file_edge=LabbookFileConnection.Edge(node=LabbookFile.create(id_data),
                                                                               cursor=cursor))


class DeleteLabbookFile(graphene.ClientIDMutation):
    class Input:
        user = graphene.String(required=True)
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        file_path = graphene.String(required=True)
        is_directory = graphene.Boolean(required=False)

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        try:
            working_directory = Configuration().config['git']['working_directory']
            inferred_lb_directory = os.path.join(working_directory, input['user'], input['owner'], 'labbooks',
                                                 input['labbook_name'])
            lb = LabBook()
            lb.from_directory(inferred_lb_directory)
            lb.delete_file(relative_path=input['file_path'], directory=input.get('is_directory') or False)
        except Exception as e:
            logger.exception(e)
            raise

        return DeleteLabbookFile(success=True)


class MoveLabbookFile(graphene.ClientIDMutation):
    """Method to move/rename a file or directory. If file, both src_path and dst_path should contain the file name.
    If a directory, be sure to include the trailing slash"""
    class Input:
        user = graphene.String(required=True)
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        src_path = graphene.String(required=True)
        dst_path = graphene.String(required=True)

    new_labbook_file_edge = graphene.Field(LabbookFileConnection.Edge)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        try:
            username = get_logged_in_username()

            working_directory = Configuration().config['git']['working_directory']
            inferred_lb_directory = os.path.join(working_directory, username, input['owner'], 'labbooks',
                                                 input['labbook_name'])
            lb = LabBook()
            lb.from_directory(inferred_lb_directory)
            file_info = lb.move_file(input['src_path'], input['dst_path'])
            logger.info(f"Moved file to `{input['dst_path']}`")

            # Create data to populate edge
            id_data = {'username': username,
                       'user': username,
                       'owner': input.get('owner'),
                       'name': input.get('labbook_name'),
                       'file_info': file_info}

            # TODO: Fix cursor implementation, this currently doesn't make sense
            cursor = base64.b64encode(f"{0}".encode('utf-8'))

        except Exception as e:
            logger.exception(e)
            raise

        return MoveLabbookFile(new_labbook_file_edge=LabbookFileConnection.Edge(node=LabbookFile.create(id_data),
                                                                                cursor=cursor))


class MakeLabbookDirectory(graphene.ClientIDMutation):
    class Input:
        user = graphene.String(required=True)
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        dir_name = graphene.String(required=True)

    new_labbook_file_edge = graphene.Field(LabbookFileConnection.Edge)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        try:
            username = get_logged_in_username()

            working_directory = Configuration().config['git']['working_directory']
            inferred_lb_directory = os.path.join(working_directory, username, input['owner'], 'labbooks',
                                                 input['labbook_name'])
            lb = LabBook()
            lb.from_directory(inferred_lb_directory)
            file_info = lb.makedir(input['dir_name'])
            logger.info(f"Made new directory in `{input['dir_name']}`")

            # Create data to populate edge
            id_data = {'username': username,
                       'user': username,
                       'owner': input.get('owner'),
                       'name': input.get('labbook_name'),
                       'file_info': file_info}

            # TODO: Fix cursor implementation, this currently doesn't make sense
            cursor = base64.b64encode(f"{0}".encode('utf-8'))

        except Exception as e:
            logger.exception(e)
            raise

        return MakeLabbookDirectory(new_labbook_file_edge=LabbookFileConnection.Edge(node=LabbookFile.create(id_data),
                                                                                     cursor=cursor))


class AddLabbookFavorite(graphene.relay.ClientIDMutation):
    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        subdir = graphene.String(required=True)
        key = graphene.String(required=True)
        description = graphene.String(required=False)
        is_dir = graphene.String(required=False)
        index = graphene.Int(required=False)

    new_favorite_edge = graphene.Field(LabbookFavoriteConnection.Edge)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        try:
            username = get_logged_in_username()
            lb = LabBook()
            lb.from_name(username, input.get('owner'), input.get('labbook_name'))

            # Add Favorite
            is_dir = False
            if input.get('is_dir'):
                is_dir = input.get('is_dir')

            new_favorite = lb.create_favorite(input.get('subdir'), input.get('key'),
                                              description=input.get('description'),
                                              position=input.get('index'),
                                              is_dir=is_dir)

            # Create data to populate edge
            id_data = {'username': username,
                       'user': username,
                       'owner': input.get('owner'),
                       'name': input.get('labbook_name'),
                       'subdir': input.get('subdir'),
                       'favorite_data': new_favorite}

            # Create cursor
            cursor = base64.b64encode(f"{str(new_favorite['index'])}".encode('utf-8'))

        except Exception as e:
            logger.exception(e)
            raise

        return AddLabbookFavorite(new_favorite_edge=LabbookFavoriteConnection.Edge(node=LabbookFavorite.create(id_data),
                                                                                   cursor=cursor))


class RemoveLabbookFavorite(graphene.ClientIDMutation):
    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        subdir = graphene.String(required=True)
        index = graphene.Int(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        try:
            username = get_logged_in_username()
            lb = LabBook()
            lb.from_name(username, input.get('owner'), input.get('labbook_name'))

            # Remove Favorite
            lb.remove_favorite(input.get('subdir'), input.get('index'))

        except Exception as e:
            logger.exception(e)
            raise

        return RemoveLabbookFavorite(success=True)
