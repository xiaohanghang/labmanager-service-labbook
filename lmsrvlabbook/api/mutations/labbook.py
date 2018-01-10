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
from lmcommon.imagebuilder import ImageBuilder
from lmcommon.activity import ActivityStore, ActivityDetailRecord, ActivityDetailType, ActivityRecord, ActivityType
from lmcommon.gitlib.gitlab import GitLabRepositoryManager

from lmsrvcore.api import logged_mutation
from lmsrvcore.api.mutations import ChunkUploadMutation, ChunkUploadInput
from lmsrvcore.auth.user import get_logged_in_username
from lmsrvcore.auth.identity import parse_token

from lmsrvlabbook.api.connections.labbookfileconnection import LabbookFavoriteConnection
from lmsrvlabbook.api.connections.labbookfileconnection import LabbookFileConnection
from lmsrvlabbook.api.objects.labbook import Labbook
from lmsrvlabbook.api.objects.labbookfile import LabbookFavorite, LabbookFile
from lmsrvlabbook.dataloader.labbook import LabBookLoader

logger = LMLogger.get_logger()


class CreateLabbook(graphene.relay.ClientIDMutation):
    """Mutator for creation of a new Labbook on disk"""

    class Input:
        name = graphene.String(required=True)
        description = graphene.String(required=True)

    # Return the LabBook instance
    labbook = graphene.Field(lambda: Labbook)

    @classmethod
    @logged_mutation
    def mutate_and_get_payload(cls, root, info, name, description, client_mutation_id=None):
        username = get_logged_in_username()

        # Create a new empty LabBook
        lb = LabBook()
        # TODO: Set owner/namespace properly once supported fully
        lb.new(owner={"username": username},
               username=username,
               name=name,
               description=description)

        # Create a Activity Store instance
        store = ActivityStore(lb)

        # Create detail record
        adr = ActivityDetailRecord(ActivityDetailType.LABBOOK, show=False, importance=0)
        adr.add_value('text/plain', f"Created new LabBook: {username}/{name}")

        # Create activity record
        ar = ActivityRecord(ActivityType.LABBOOK,
                            message=f"Created new LabBook: {username}/{name}",
                            show=True,
                            importance=255,
                            linked_commit=lb.git.commit_hash)
        ar.add_detail_object(adr)

        # Store
        store.create_activity_record(ar)

        # Prime dataloader with labbook you just created
        dataloader = LabBookLoader()
        dataloader.prime(f"{username}&{username}&{lb.name}", lb)

        # Get a graphene instance of the newly created LabBook
        return CreateLabbook(labbook=Labbook(owner=username, name=lb.name, _dataloader=dataloader))


class RenameLabbook(graphene.ClientIDMutation):
    """Rename a labbook"""
    class Input:
        owner = graphene.String(required=True)
        original_labbook_name = graphene.String(required=True)
        new_labbook_name = graphene.String(required=True)

    success = graphene.Boolean()

    @classmethod
    @logged_mutation
    def mutate_and_get_payload(cls, input, context, info):
        # This bypasses the original implementation. Rename is temporarily disabled.
        raise NotImplemented('Rename functionality is temporarily disabled.')

    @classmethod
    @logged_mutation
    def prior_mutate_and_get_payload(cls, input, context, info):
        # NOTE!!! This is the code that was originally to rename.
        # Temporarily, rename functionality is disabled.
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

        return RenameLabbook(success=True)


class ExportLabbook(graphene.relay.ClientIDMutation):
    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)

    job_key = graphene.String()

    @classmethod
    @logged_mutation
    def mutate_and_get_payload(cls, input, context, info):
        username = get_logged_in_username()
        logger.info(f'Exporting LabBook: {username}/{input["owner"]}/{input["labbook_name"]}')

        working_directory = Configuration().config['git']['working_directory']
        inferred_lb_directory = os.path.join(working_directory, username, input['owner'], 'labbooks',
                                             input['labbook_name'])
        lb = LabBook()
        lb.from_directory(inferred_lb_directory)

        job_metadata = {'method': 'export_labbook_as_zip', 'labbook': lb.root_dir}
        job_kwargs = {'labbook_path': lb.root_dir, 'lb_export_directory': os.path.join(working_directory, 'export')}
        dispatcher = Dispatcher()
        job_key = dispatcher.dispatch_task(jobs.export_labbook_as_zip, kwargs=job_kwargs, metadata=job_metadata)
        logger.info(f"Exporting LabBook {lb.root_dir} in background job with key {job_key.key_str}")

        return ExportLabbook(job_key=job_key.key_str)


class ImportLabbook(graphene.relay.ClientIDMutation, ChunkUploadMutation):
    class Input:
        chunk_upload_params = ChunkUploadInput(required=True)

    import_job_key = graphene.String()
    build_image_job_key = graphene.String()

    @classmethod
    @logged_mutation
    def mutate_and_process_upload(cls, input, context, info):
        if not cls.upload_file_path:
            logger.error('No file uploaded')
            raise ValueError('No file uploaded')

        username = get_logged_in_username()
        logger.info(
            f"Handling ImportLabbook mutation: user={username},"
            f"owner={username}. Uploaded file {cls.upload_file_path}")

        job_metadata = {'method': 'import_labbook_from_zip'}
        job_kwargs = {
            'archive_path': cls.upload_file_path,
            'username': username,
            'owner': username,
            'base_filename': cls.filename
        }
        dispatcher = Dispatcher()
        job_key = dispatcher.dispatch_task(jobs.import_labboook_from_zip, kwargs=job_kwargs, metadata=job_metadata)
        logger.info(f"Importing LabBook {cls.upload_file_path} in background job with key {job_key.key_str}")

        assumed_lb_name = cls.filename.replace('.lbk', '').split('_')[0]
        working_directory = Configuration().config['git']['working_directory']
        inferred_lb_directory = os.path.join(working_directory, username, username, 'labbooks',
                                             assumed_lb_name)
        build_img_kwargs = {
            'path': os.path.join(inferred_lb_directory, '.gigantum', 'env'),
            'tag': f"{username}-{username}-{assumed_lb_name}",
            'pull': True,
            'nocache': False
        }
        build_img_metadata = {
            'method': 'build_image',
            'labbook': f"{username}-{username}-{assumed_lb_name}"
        }
        logger.info(f"Queueing job to build imported labbook at assumed directory `{inferred_lb_directory}`")
        build_image_job_key = dispatcher.dispatch_task(jobs.build_docker_image, kwargs=build_img_kwargs,
                                                       dependent_job=job_key, metadata=build_img_metadata)
        logger.info(f"Adding dependent job {build_image_job_key} to build "
                    f"Docker image for labbook `{inferred_lb_directory}`")

        return ImportLabbook(import_job_key=job_key.key_str, build_image_job_key=build_image_job_key.key_str)


class ImportRemoteLabbook(graphene.relay.ClientIDMutation):
    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        remote_url = graphene.String(required=True)

    active_branch = graphene.String()

    @classmethod
    @logged_mutation
    def mutate_and_get_payload(cls, input, context, info):
        username = get_logged_in_username()
        logger.info(f"Importing remote labbook from {input.get('remote_url')}")
        lb = LabBook()

        # TODO: Future work will look up remote in LabBook data, allowing user to select remote.
        default_remote = lb.labmanager_config.config['git']['default_remote']
        admin_service = None
        for remote in lb.labmanager_config.config['git']['remotes']:
            if default_remote == remote:
                admin_service = lb.labmanager_config.config['git']['remotes'][remote]['admin_service']
                break

        # Extract valid Bearer token
        if hasattr(context, 'headers') and "HTTP_AUTHORIZATION" in context.headers.environ:
            token = parse_token(context.headers.environ["HTTP_AUTHORIZATION"])
        else:
            raise ValueError("Authorization header not provided. Must have a valid session to query for collaborators")

        mgr = GitLabRepositoryManager(default_remote, admin_service, token,
                                      username, input.get('owner'), input.get('labbook_name'))
        mgr.configure_git_credentials(default_remote, username)

        lb.from_remote(input['remote_url'], username, input['owner'], input['labbook_name'])
        return ImportRemoteLabbook(active_branch=lb.active_branch)


class AddLabbookRemote(graphene.relay.ClientIDMutation):
    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        remote_name = graphene.String(required=True)
        remote_url = graphene.String(required=True)

    success = graphene.Boolean()

    @classmethod
    @logged_mutation
    def mutate_and_get_payload(cls, input, context, info):
        username = get_logged_in_username()
        logger.info(f"Adding labbook remote {input.get('remote_name')} {input.get('remote_url')}")

        lb = LabBook()
        lb.from_name(username, input.get('owner'), input.get('labbook_name'))
        remote = input.get('remote_name')
        lb.add_remote(remote, input.get('remote_url'))
        return AddLabbookRemote(success=True)


class PullActiveBranchFromRemote(graphene.relay.ClientIDMutation):
    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        remote_name = graphene.String(required=False)

    success = graphene.Boolean()

    @classmethod
    @logged_mutation
    def mutate_and_get_payload(cls, input, context, info):
        username = get_logged_in_username()
        logger.info(f"Importing remote labbook from {input.get('remote_name')}")
        lb = LabBook()
        lb.from_name(username, input.get('owner'), input.get('labbook_name'))
        remote = input.get('remote_name')
        if remote:
            lb.pull(remote=remote)
        else:
            lb.pull()
        return PullActiveBranchFromRemote(success=True)


class PushActiveBranchToRemote(graphene.relay.ClientIDMutation):
    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        remote_name = graphene.String(required=False)

    success = graphene.Boolean()

    @classmethod
    @logged_mutation
    def mutate_and_get_payload(cls, input, context, info):
        username = get_logged_in_username()
        logger.info(f"Importing remote labbook from {input.get('remote_name')}")
        lb = LabBook()
        lb.from_name(username, input.get('owner'), input.get('labbook_name'))
        remote = input.get('remote_name')
        if remote:
            lb.push(remote=remote)
        else:
            lb.push()
        return PushActiveBranchToRemote(success=True)


class AddLabbookFile(graphene.relay.ClientIDMutation, ChunkUploadMutation):
    """Mutation to add a file to a labbook. File should be sent in the `uploadFile` key as a multi-part/form upload.
    file_path is the relative path from the labbook section specified."""
    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        section = graphene.String(required=True)
        file_path = graphene.String(required=True)
        chunk_upload_params = ChunkUploadInput(required=True)

    new_labbook_file_edge = graphene.Field(LabbookFileConnection.Edge)

    @classmethod
    @logged_mutation
    def mutate_and_process_upload(cls, input, context, info):
        if not cls.upload_file_path:
            logger.error('No file uploaded')
            raise ValueError('No file uploaded')

        username = get_logged_in_username()
        working_directory = Configuration().config['git']['working_directory']
        inferred_lb_directory = os.path.join(working_directory, username, input['owner'], 'labbooks',
                                             input['labbook_name'])
        lb = LabBook()
        lb.from_directory(inferred_lb_directory)

        # Insert into labbook
        # Note: insert_file() will strip out any '..' in dst_dir.
        file_info = lb.insert_file(section=input['section'],
                                   src_file=cls.upload_file_path,
                                   dst_dir=os.path.dirname(input['file_path']),
                                   base_filename=cls.filename)

        logger.debug(f"Removing copied temp file {cls.upload_file_path}")
        os.remove(cls.upload_file_path)
        # Create data to populate edge
        id_data = {'username': username,
                   'owner': input.get('owner'),
                   'name': input.get('labbook_name'),
                   'section': input['section'],
                   'file_info': file_info}

        # TODO: Fix cursor implementation, this currently doesn't make sense when adding edges
        cursor = base64.b64encode(f"{0}".encode('utf-8'))
        return AddLabbookFile(new_labbook_file_edge=LabbookFileConnection.Edge(node=LabbookFile.create(id_data),
                                                                               cursor=cursor))


class DeleteLabbookFile(graphene.ClientIDMutation):
    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        section = graphene.String(required=True)
        file_path = graphene.String(required=True)
        is_directory = graphene.Boolean(required=False)

    success = graphene.Boolean()

    @classmethod
    @logged_mutation
    def mutate_and_get_payload(cls, input, context, info):
        username = get_logged_in_username()
        working_directory = Configuration().config['git']['working_directory']
        inferred_lb_directory = os.path.join(working_directory, username, input['owner'], 'labbooks',
                                             input['labbook_name'])
        lb = LabBook()
        lb.from_directory(inferred_lb_directory)
        lb.delete_file(section=input['section'], relative_path=input['file_path'],
                       directory=input.get('is_directory') or False)

        return DeleteLabbookFile(success=True)


class MoveLabbookFile(graphene.ClientIDMutation):
    """Method to move/rename a file or directory. If file, both src_path and dst_path should contain the file name.
    If a directory, be sure to include the trailing slash"""
    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        section = graphene.String(required=True)
        src_path = graphene.String(required=True)
        dst_path = graphene.String(required=True)

    new_labbook_file_edge = graphene.Field(LabbookFileConnection.Edge)

    @classmethod
    @logged_mutation
    def mutate_and_get_payload(cls, input, context, info):
        username = get_logged_in_username()

        working_directory = Configuration().config['git']['working_directory']
        inferred_lb_directory = os.path.join(working_directory, username, input['owner'], 'labbooks',
                                             input['labbook_name'])
        lb = LabBook()
        lb.from_directory(inferred_lb_directory)
        file_info = lb.move_file(input['section'], input['src_path'], input['dst_path'])
        logger.info(f"Moved file to `{input['dst_path']}`")

        # Create data to populate edge
        id_data = {'username': username,
                   'user': username,
                   'owner': input.get('owner'),
                   'name': input.get('labbook_name'),
                   'section': input.get('section'),
                   'file_info': file_info}

        # TODO: Fix cursor implementation, this currently doesn't make sense
        cursor = base64.b64encode(f"{0}".encode('utf-8'))

        return MoveLabbookFile(new_labbook_file_edge=LabbookFileConnection.Edge(node=LabbookFile.create(id_data),
                                                                                cursor=cursor))


class MakeLabbookDirectory(graphene.ClientIDMutation):
    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        section = graphene.String(required=True)
        directory = graphene.String(required=True)

    new_labbook_file_edge = graphene.Field(LabbookFileConnection.Edge)

    @classmethod
    @logged_mutation
    def mutate_and_get_payload(cls, input, context, info):
        username = get_logged_in_username()

        working_directory = Configuration().config['git']['working_directory']
        inferred_lb_directory = os.path.join(working_directory, username, input['owner'], 'labbooks',
                                             input['labbook_name'])
        lb = LabBook()
        lb.from_directory(inferred_lb_directory)
        lb.makedir(os.path.join(input['section'], input['directory']), create_activity_record=True)
        logger.info(f"Made new directory in `{input['directory']}`")

        # Create data to populate edge
        id_data = {'username': username,
                   'user': username,
                   'owner': input.get('owner'),
                   'name': input.get('labbook_name'),
                   'section': input.get('section'),
                   'file_info': lb.get_file_info(input['section'], input['directory'])}

        # TODO: Fix cursor implementation, this currently doesn't make sense
        cursor = base64.b64encode(f"{0}".encode('utf-8'))

        return MakeLabbookDirectory(new_labbook_file_edge=LabbookFileConnection.Edge(node=LabbookFile.create(id_data),
                                                                                     cursor=cursor))


class AddLabbookFavorite(graphene.relay.ClientIDMutation):
    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        section = graphene.String(required=True)
        key = graphene.String(required=True)
        description = graphene.String(required=False)
        is_dir = graphene.Boolean(required=False)
        index = graphene.Int(required=False)

    new_favorite_edge = graphene.Field(LabbookFavoriteConnection.Edge)

    @classmethod
    @logged_mutation
    def mutate_and_get_payload(cls, input, context, info):
        username = get_logged_in_username()
        lb = LabBook()
        lb.from_name(username, input.get('owner'), input.get('labbook_name'))

        # Add Favorite
        is_dir = False
        if input.get('is_dir'):
            is_dir = input.get('is_dir')

        new_favorite = lb.create_favorite(input.get('section'), input.get('key'),
                                          description=input.get('description'),
                                          position=input.get('index'),
                                          is_dir=is_dir)

        # Create data to populate edge
        id_data = {'username': username,
                   'owner': input.get('owner'),
                   'name': input.get('labbook_name'),
                   'section': input.get('section'),
                   'favorite_data': new_favorite}

        # Create cursor
        cursor = base64.b64encode(f"{str(new_favorite['index'])}".encode('utf-8'))

        return AddLabbookFavorite(new_favorite_edge=LabbookFavoriteConnection.Edge(node=LabbookFavorite.create(id_data),
                                                                                   cursor=cursor))


class UpdateLabbookFavorite(graphene.relay.ClientIDMutation):
    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        section = graphene.String(required=True)
        index = graphene.Int(required=True)
        updated_index = graphene.Int(required=False)
        updated_key = graphene.String(required=False)
        updated_description = graphene.String(required=False)

    updated_favorite_edge = graphene.Field(LabbookFavoriteConnection.Edge)

    @classmethod
    @logged_mutation
    def mutate_and_get_payload(cls, input, context, info):
        username = get_logged_in_username()
        lb = LabBook()
        lb.from_name(username, input.get('owner'), input.get('labbook_name'))

        # Update Favorite
        new_favorite = lb.update_favorite(input.get('section'), input.get('index'),
                                          new_description=input.get('updated_description'),
                                          new_index=input.get('updated_index'),
                                          new_key=input.get('updated_key'))

        # Create data to populate edge
        id_data = {'username': username,
                   'user': username,
                   'owner': input.get('owner'),
                   'name': input.get('labbook_name'),
                   'section': input.get('section'),
                   'favorite_data': new_favorite}

        # Create dummy cursor
        cursor = base64.b64encode(f"{str(new_favorite['index'])}".encode('utf-8'))

        return UpdateLabbookFavorite(updated_favorite_edge=LabbookFavoriteConnection.Edge(node=LabbookFavorite.create(id_data),
                                                                                          cursor=cursor))


class RemoveLabbookFavorite(graphene.ClientIDMutation):
    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        section = graphene.String(required=True)
        index = graphene.Int(required=True)

    success = graphene.Boolean()

    @classmethod
    @logged_mutation
    def mutate_and_get_payload(cls, input, context, info):
        username = get_logged_in_username()
        lb = LabBook()
        lb.from_name(username, input.get('owner'), input.get('labbook_name'))

        # Remove Favorite
        lb.remove_favorite(input.get('section'), input.get('index'))

        return RemoveLabbookFavorite(success=True)


class AddLabbookCollaborator(graphene.relay.ClientIDMutation):
    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        username = graphene.String(required=True)

    updated_labbook = graphene.Field(Labbook)

    @classmethod
    @logged_mutation
    def mutate_and_get_payload(cls, input, context, info):
        username = get_logged_in_username()
        lb = LabBook()
        lb.from_name(username, input.get('owner'), input.get('labbook_name'))

        # TODO: Future work will look up remote in LabBook data, allowing user to select remote.
        default_remote = lb.labmanager_config.config['git']['default_remote']
        admin_service = None
        for remote in lb.labmanager_config.config['git']['remotes']:
            if default_remote == remote:
                admin_service = lb.labmanager_config.config['git']['remotes'][remote]['admin_service']
                break

        # Extract valid Bearer token
        if "HTTP_AUTHORIZATION" in context.headers.environ:
            token = parse_token(context.headers.environ["HTTP_AUTHORIZATION"])
        else:
            raise ValueError("Authorization header not provided. Must have a valid session to query for collaborators")

        # Add collaborator to remote service
        mgr = GitLabRepositoryManager(default_remote, admin_service, token,
                                      username, input.get('owner'), input.get('labbook_name'))
        mgr.add_collaborator(input.get('username'))

        id_data = {"owner": input.get('owner'),
                   "name": input.get('labbook_name'),
                   "username": username}
        return AddLabbookCollaborator(updated_labbook=Labbook.create(id_data=id_data))


class DeleteLabbookCollaborator(graphene.relay.ClientIDMutation):
    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        username = graphene.String(required=True)

    updated_labbook = graphene.Field(Labbook)

    @classmethod
    @logged_mutation
    def mutate_and_get_payload(cls, input, context, info):
        username = get_logged_in_username()
        lb = LabBook()
        lb.from_name(username, input.get('owner'), input.get('labbook_name'))

        # TODO: Future work will look up remote in LabBook data, allowing user to select remote.
        default_remote = lb.labmanager_config.config['git']['default_remote']
        admin_service = None
        for remote in lb.labmanager_config.config['git']['remotes']:
            if default_remote == remote:
                admin_service = lb.labmanager_config.config['git']['remotes'][remote]['admin_service']
                break

        # Extract valid Bearer token
        if "HTTP_AUTHORIZATION" in context.headers.environ:
            token = parse_token(context.headers.environ["HTTP_AUTHORIZATION"])
        else:
            raise ValueError("Authorization header not provided. Must have a valid session to query for collaborators")

        # Add collaborator to remote service
        mgr = GitLabRepositoryManager(default_remote, admin_service, token,
                                      username, input.get('owner'), input.get('labbook_name'))
        mgr.delete_collaborator(input.get('username'))

        id_data = {"owner": input.get('owner'),
                   "name": input.get('labbook_name'),
                   "username": username}
        return DeleteLabbookCollaborator(updated_labbook=Labbook.create(id_data=id_data))
