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
import os
import uuid
import tempfile
import base64
import json

import graphene

from lmcommon.configuration import Configuration
from lmcommon.dispatcher import (Dispatcher, jobs)
from lmcommon.labbook import LabBook
from lmcommon.logging import LMLogger
from lmcommon.notes import NoteStore, NoteLogLevel
from lmsrvcore.auth.user import get_logged_in_username
from lmsrvlabbook.api.objects.labbook import Labbook

from lmsrvlabbook.api.objects.labbookfile import LabbookFavorite, LabbookFile
from lmsrvlabbook.api.connections.labbookfileconnection import LabbookFavoriteConnection
from lmsrvlabbook.api.connections.labbookfileconnection import LabbookFileConnection

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


class ImportLabbook(graphene.relay.ClientIDMutation):

    class Input:
        owner = graphene.String(required=True)
        user = graphene.String(required=True)

    import_job_key = graphene.String()
    build_image_job_key = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        if not context.files.get('archiveFile'):
            logger.error('No file "archiveFile" associated with request')
            raise ValueError('No file archiveFile in request context')

        logger.info(
            f"Handling ImportLabbook mutation: user={input.get('user')},"
            f"owner={input.get('owner')}. Uploaded file {context.files.get('archiveFile').filename}")

        # Create a new unique directory in /tmp
        archive_temp_dir = os.path.join(tempfile.gettempdir(), 'labbook_imports', str(uuid.uuid4()))
        logger.info(f"Making new directory in {archive_temp_dir}")
        os.makedirs(archive_temp_dir, exist_ok=True)

        labbook_archive_path = os.path.join(archive_temp_dir, context.files['archiveFile'].filename)
        context.files.get('archiveFile').save(labbook_archive_path)

        job_metadata = {'method': 'import_labbook_from_zip'}
        job_kwargs = {
            'archive_path': labbook_archive_path,
            'username': input.get('user'),
            'owner': input.get('owner')
        }
        dispatcher = Dispatcher()
        job_key = dispatcher.dispatch_task(jobs.import_labboook_from_zip, kwargs=job_kwargs, metadata=job_metadata)
        logger.info(f"Importing LabBook {labbook_archive_path} in background job with key {job_key.key_str}")

        assumed_lb_name = context.files['archiveFile'].filename.replace('.lbk', '').split('_')[0]
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


class AddLabbookFile(graphene.relay.ClientIDMutation):
    """Mutation to add a file to a labbook. File should be sent in the `newFile` key as a multi-part/form upload.
    file_path is the relative path from the labbook root."""
    class Input:
        user = graphene.String(required=True)
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        file_path = graphene.String(required=True)

    new_labbook_file_edge = graphene.Field(LabbookFileConnection.Edge)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        if not context.files.get('newFile'):
            logger.error('No file "newFile" associated with request')
            raise ValueError('No file newFile in request context')

        try:
            username = get_logged_in_username()

            working_directory = Configuration().config['git']['working_directory']
            inferred_lb_directory = os.path.join(working_directory, username, input['owner'], 'labbooks',
                                                 input['labbook_name'])
            lb = LabBook()
            lb.from_directory(inferred_lb_directory)

            if os.path.basename(context.files['newFile'].filename) != os.path.basename(input['file_path']):
                raise ValueError('Filename of request file and `file_path` do not match')

            # Create a new unique directory in /tmp
            labbook_archive_path = os.path.join(tempfile.gettempdir(), uuid.uuid4().hex)
            os.makedirs(labbook_archive_path)

            # Write file to temp space
            labbook_archive_path = os.path.join(labbook_archive_path,
                                                os.path.basename(context.files['newFile'].filename))
            context.files.get('newFile').save(labbook_archive_path)

            # Insert into labbook
            new_path = lb.insert_file(src_file=labbook_archive_path, dst_dir=os.path.dirname(input['file_path']))

            logger.debug(f"Removing copied temp file {labbook_archive_path}")
            os.remove(labbook_archive_path)

            # Create data to populate edge
            file_info = os.stat(new_path)
            file_data = {
                          'key': input['file_path'],
                          'is_dir': False,
                          'size': file_info.st_size,
                          'modified_at': file_info.st_mtime
                        }
            id_data = {'username': username,
                       'user': username,
                       'owner': input.get('owner'),
                       'name': input.get('labbook_name'),
                       'enc_file_data': base64.b64encode(json.dumps(file_data).encode())}

            # TODO: Fix cursor implementation, this currently doesn't make sense
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

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        try:
            working_directory = Configuration().config['git']['working_directory']
            inferred_lb_directory = os.path.join(working_directory, input['user'], input['owner'], 'labbooks',
                                                 input['labbook_name'])
            lb = LabBook()
            lb.from_directory(inferred_lb_directory)
            lb.delete_file(relative_path=input['file_path'])
        except Exception as e:
            logger.exception(e)
            raise

        return DeleteLabbookFile(success=True)


class MoveLabbookFile(graphene.ClientIDMutation):
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
            full_path = lb.move_file(input['src_path'], input['dst_path'])
            logger.info(f"Moved file to `{full_path}`")

            # Create data to populate edge
            file_info = os.stat(full_path)
            file_data = {
                'key': input['dst_path'],
                'is_dir': False,
                'size': file_info.st_size,
                'modified_at': file_info.st_mtime
            }
            id_data = {'username': username,
                       'user': username,
                       'owner': input.get('owner'),
                       'name': input.get('labbook_name'),
                       'enc_file_data': base64.b64encode(json.dumps(file_data).encode())}

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
            full_path = lb.makedir(input['dir_name'])
            logger.info(f"Made new directory in `{full_path}`")

            # Create data to populate edge
            file_info = os.stat(full_path)
            file_data = {
                'key': input['dir_name'],
                'is_dir': True,
                'size': file_info.st_size,
                'modified_at': file_info.st_mtime
            }
            id_data = {'username': username,
                       'user': username,
                       'owner': input.get('owner'),
                       'name': input.get('labbook_name'),
                       'enc_file_data': base64.b64encode(json.dumps(file_data).encode())}

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
