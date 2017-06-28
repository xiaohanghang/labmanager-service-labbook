# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_create_note 1'] = {
    'data': {
        'note': {
            'labbookName': 'notes-test-1',
            'author': "{'name': 'Gigantum AutoCommit', 'email': 'noreply@gigantum.io'}",
            'message': 'Added a new file in this test',
            'level': 'USER_MINOR',
            'tags': [
                'user',
                'minor'
            ],
            'freeText': 'Lots of stuff can go here <>><<>::SDF:',
            'objects': [
                {
                    'key': 'objectkey1',
                    'objectType': 'PNG',
                    'value': '2new0x7FABC374FX'
                }
            ]
        }
    }
}

snapshots['test_get_note_summaries 1'] = {
    'data': {
        'createNote': {
            'note': {
                'labbookName': 'notes-test-2',
                'author': None,
                'message': 'Added a new file in this test 0',
                'level': 'USER_MINOR',
                'tags': [
                    'user',
                    'minor'
                ],
                'freeText': 'Lots of stuff can go here <>><<>::SDF:',
                'objects': [
                    {
                        'key': 'objectkey1',
                        'objectType': 'PNG',
                        'value': '2new0x7FABC374FX'
                    }
                ]
            }
        }
    }
}

snapshots['test_get_note_summaries 2'] = {
    'data': {
        'createNote': {
            'note': {
                'labbookName': 'notes-test-2',
                'author': None,
                'message': 'Added a new file in this test 1',
                'level': 'USER_MINOR',
                'tags': [
                    'user',
                    'minor'
                ],
                'freeText': 'Lots of stuff can go here <>><<>::SDF:',
                'objects': [
                    {
                        'key': 'objectkey1',
                        'objectType': 'PNG',
                        'value': '2new0x7FABC374FX'
                    }
                ]
            }
        }
    }
}

snapshots['test_get_note_summaries 3'] = {
    'data': {
        'createNote': {
            'note': {
                'labbookName': 'notes-test-2',
                'author': None,
                'message': 'Added a new file in this test 2',
                'level': 'USER_MINOR',
                'tags': [
                    'user',
                    'minor'
                ],
                'freeText': 'Lots of stuff can go here <>><<>::SDF:',
                'objects': [
                    {
                        'key': 'objectkey1',
                        'objectType': 'PNG',
                        'value': '2new0x7FABC374FX'
                    }
                ]
            }
        }
    }
}

snapshots['test_get_note_summaries 4'] = {
    'data': {
        'createNote': {
            'note': {
                'labbookName': 'notes-test-2',
                'author': None,
                'message': 'Added a new file in this test 3',
                'level': 'USER_MINOR',
                'tags': [
                    'user',
                    'minor'
                ],
                'freeText': 'Lots of stuff can go here <>><<>::SDF:',
                'objects': [
                    {
                        'key': 'objectkey1',
                        'objectType': 'PNG',
                        'value': '2new0x7FABC374FX'
                    }
                ]
            }
        }
    }
}

snapshots['test_get_note_summaries 5'] = {
    'data': {
        'createNote': {
            'note': {
                'labbookName': 'notes-test-2',
                'author': None,
                'message': 'Added a new file in this test 4',
                'level': 'USER_MINOR',
                'tags': [
                    'user',
                    'minor'
                ],
                'freeText': 'Lots of stuff can go here <>><<>::SDF:',
                'objects': [
                    {
                        'key': 'objectkey1',
                        'objectType': 'PNG',
                        'value': '2new0x7FABC374FX'
                    }
                ]
            }
        }
    }
}

snapshots['test_get_note_summaries 6'] = {
    'data': {
        'noteSummaries': {
            'entries': [
                {
                    'labbookName': 'notes-test-2',
                    'author': "{'name': 'Gigantum AutoCommit', 'email': 'noreply@gigantum.io'}",
                    'level': 'USER_MINOR',
                    'message': 'Added a new file in this test 4',
                    'tags': [
                        'user',
                        'minor'
                    ]
                },
                {
                    'labbookName': 'notes-test-2',
                    'author': "{'name': 'Gigantum AutoCommit', 'email': 'noreply@gigantum.io'}",
                    'level': 'USER_MINOR',
                    'message': 'Added a new file in this test 3',
                    'tags': [
                        'user',
                        'minor'
                    ]
                },
                {
                    'labbookName': 'notes-test-2',
                    'author': "{'name': 'Gigantum AutoCommit', 'email': 'noreply@gigantum.io'}",
                    'level': 'USER_MINOR',
                    'message': 'Added a new file in this test 2',
                    'tags': [
                        'user',
                        'minor'
                    ]
                },
                {
                    'labbookName': 'notes-test-2',
                    'author': "{'name': 'Gigantum AutoCommit', 'email': 'noreply@gigantum.io'}",
                    'level': 'USER_MINOR',
                    'message': 'Added a new file in this test 1',
                    'tags': [
                        'user',
                        'minor'
                    ]
                },
                {
                    'labbookName': 'notes-test-2',
                    'author': "{'name': 'Gigantum AutoCommit', 'email': 'noreply@gigantum.io'}",
                    'level': 'USER_MINOR',
                    'message': 'Added a new file in this test 0',
                    'tags': [
                        'user',
                        'minor'
                    ]
                }
            ]
        }
    }
}
