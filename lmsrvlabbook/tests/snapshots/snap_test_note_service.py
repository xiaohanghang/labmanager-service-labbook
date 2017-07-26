# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestNoteService.test_create_note 1'] = {
    'data': {
        'labbook': {
            'notes': {
                'edges': [
                    {
                        'node': {
                            'message': 'Added a new file in this test'
                        }
                    }
                ]
            }
        }
    }
}

snapshots['TestNoteService.test_get_note_summaries 1'] = {
    'data': {
        'createNote': {
            'note': {
                'author': 'noreply@gigantum.io',
                'freeText': 'Lots of stuff can go here <>><<>::SDF:',
                'level': 'USER_MINOR',
                'message': 'Added a new file in this test 0',
                'tags': [
                    'minor',
                    'user'
                ]
            }
        }
    }
}

snapshots['TestNoteService.test_get_note_summaries 2'] = {
    'data': {
        'createNote': {
            'note': {
                'author': 'noreply@gigantum.io',
                'freeText': 'Lots of stuff can go here <>><<>::SDF:',
                'level': 'USER_MINOR',
                'message': 'Added a new file in this test 1',
                'tags': [
                    'minor',
                    'user'
                ]
            }
        }
    }
}

snapshots['TestNoteService.test_get_note_summaries 3'] = {
    'data': {
        'createNote': {
            'note': {
                'author': 'noreply@gigantum.io',
                'freeText': 'Lots of stuff can go here <>><<>::SDF:',
                'level': 'USER_MINOR',
                'message': 'Added a new file in this test 2',
                'tags': [
                    'minor',
                    'user'
                ]
            }
        }
    }
}

snapshots['TestNoteService.test_get_note_summaries 4'] = {
    'data': {
        'createNote': {
            'note': {
                'author': 'noreply@gigantum.io',
                'freeText': 'Lots of stuff can go here <>><<>::SDF:',
                'level': 'USER_MINOR',
                'message': 'Added a new file in this test 3',
                'tags': [
                    'minor',
                    'user'
                ]
            }
        }
    }
}

snapshots['TestNoteService.test_get_note_summaries 5'] = {
    'data': {
        'createNote': {
            'note': {
                'author': 'noreply@gigantum.io',
                'freeText': 'Lots of stuff can go here <>><<>::SDF:',
                'level': 'USER_MINOR',
                'message': 'Added a new file in this test 4',
                'tags': [
                    'minor',
                    'user'
                ]
            }
        }
    }
}

snapshots['TestNoteService.test_get_note_summaries 6'] = {
    'data': {
        'labbook': {
            'notes': {
                'edges': [
                    {
                        'node': {
                            'author': 'noreply@gigantum.io',
                            'level': 'USER_MINOR',
                            'message': 'Added a new file in this test 4',
                            'tags': [
                                'minor',
                                'user'
                            ]
                        }
                    },
                    {
                        'node': {
                            'author': 'noreply@gigantum.io',
                            'level': 'USER_MINOR',
                            'message': 'Added a new file in this test 3',
                            'tags': [
                                'minor',
                                'user'
                            ]
                        }
                    },
                    {
                        'node': {
                            'author': 'noreply@gigantum.io',
                            'level': 'USER_MINOR',
                            'message': 'Added a new file in this test 2',
                            'tags': [
                                'minor',
                                'user'
                            ]
                        }
                    },
                    {
                        'node': {
                            'author': 'noreply@gigantum.io',
                            'level': 'USER_MINOR',
                            'message': 'Added a new file in this test 1',
                            'tags': [
                                'minor',
                                'user'
                            ]
                        }
                    },
                    {
                        'node': {
                            'author': 'noreply@gigantum.io',
                            'level': 'USER_MINOR',
                            'message': 'Added a new file in this test 0',
                            'tags': [
                                'minor',
                                'user'
                            ]
                        }
                    }
                ]
            }
        }
    }
}

snapshots['TestNoteService.test_get_full_note 1'] = {
    'data': {
        'labbook': {
            'notes': {
                'edges': [
                    {
                        'cursor': 'MA==',
                        'node': {
                            'author': 'noreply@gigantum.io',
                            'freeText': 'Lots of stuff can go here <>><<>::SDF:',
                            'level': 'USER_MINOR',
                            'message': 'Added a new file in this test',
                            'objects': {
                                'edges': [
                                    {
                                        'cursor': 'MA==',
                                        'node': {
                                            'key': 'objectkey1',
                                            'type': 'PNG',
                                            'value': "b'\\xdaw\\xb0\\xd3\\x1e\\xc5\\x00\\x10\\xb7\\xef\\x81W'"
                                        }
                                    },
                                    {
                                        'cursor': 'MQ==',
                                        'node': {
                                            'key': 'objectkey2',
                                            'type': 'BLOB',
                                            'value': "b'asdfasdffgdhasd1243'"
                                        }
                                    }
                                ]
                            },
                            'tags': [
                                'minor',
                                'user'
                            ]
                        }
                    }
                ]
            }
        }
    }
}
