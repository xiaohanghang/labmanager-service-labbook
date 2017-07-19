# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_create_note 1'] = {
    'data': {
        'note': {
            'author': "{'name': 'Gigantum AutoCommit', 'email': 'noreply@gigantum.io'}",
            'freeText': 'Lots of stuff can go here <>><<>::SDF:',
            'labbookName': 'notes-test-1',
            'level': 'USER_MINOR',
            'message': 'Added a new file in this test',
            'objects': [
                {
                    'key': 'objectkey1',
                    'objectType': 'PNG',
                    'value': '2new0x7FABC374FX'
                }
            ],
            'tags': [
                'user',
                'minor'
            ]
        }
    }
}

snapshots['test_get_note_summaries 1'] = {
    'data': {
        'createNote': {
            'note': {
                'author': None,
                'freeText': 'Lots of stuff can go here <>><<>::SDF:',
                'labbookName': 'notes-test-2',
                'level': 'USER_MINOR',
                'message': 'Added a new file in this test 0',
                'objects': [
                    {
                        'key': 'objectkey1',
                        'objectType': 'PNG',
                        'value': '2new0x7FABC374FX'
                    }
                ],
                'tags': [
                    'user',
                    'minor'
                ]
            }
        }
    }
}

snapshots['test_get_note_summaries 2'] = {
    'data': {
        'createNote': {
            'note': {
                'author': None,
                'freeText': 'Lots of stuff can go here <>><<>::SDF:',
                'labbookName': 'notes-test-2',
                'level': 'USER_MINOR',
                'message': 'Added a new file in this test 1',
                'objects': [
                    {
                        'key': 'objectkey1',
                        'objectType': 'PNG',
                        'value': '2new0x7FABC374FX'
                    }
                ],
                'tags': [
                    'user',
                    'minor'
                ]
            }
        }
    }
}

snapshots['test_get_note_summaries 3'] = {
    'data': {
        'createNote': {
            'note': {
                'author': None,
                'freeText': 'Lots of stuff can go here <>><<>::SDF:',
                'labbookName': 'notes-test-2',
                'level': 'USER_MINOR',
                'message': 'Added a new file in this test 2',
                'objects': [
                    {
                        'key': 'objectkey1',
                        'objectType': 'PNG',
                        'value': '2new0x7FABC374FX'
                    }
                ],
                'tags': [
                    'user',
                    'minor'
                ]
            }
        }
    }
}

snapshots['test_get_note_summaries 4'] = {
    'data': {
        'createNote': {
            'note': {
                'author': None,
                'freeText': 'Lots of stuff can go here <>><<>::SDF:',
                'labbookName': 'notes-test-2',
                'level': 'USER_MINOR',
                'message': 'Added a new file in this test 3',
                'objects': [
                    {
                        'key': 'objectkey1',
                        'objectType': 'PNG',
                        'value': '2new0x7FABC374FX'
                    }
                ],
                'tags': [
                    'user',
                    'minor'
                ]
            }
        }
    }
}

snapshots['test_get_note_summaries 5'] = {
    'data': {
        'createNote': {
            'note': {
                'author': None,
                'freeText': 'Lots of stuff can go here <>><<>::SDF:',
                'labbookName': 'notes-test-2',
                'level': 'USER_MINOR',
                'message': 'Added a new file in this test 4',
                'objects': [
                    {
                        'key': 'objectkey1',
                        'objectType': 'PNG',
                        'value': '2new0x7FABC374FX'
                    }
                ],
                'tags': [
                    'user',
                    'minor'
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
                    'author': "{'name': 'Gigantum AutoCommit', 'email': 'noreply@gigantum.io'}",
                    'labbookName': 'notes-test-2',
                    'level': 'USER_MINOR',
                    'message': 'Added a new file in this test 4',
                    'tags': [
                        'user',
                        'minor'
                    ]
                },
                {
                    'author': "{'name': 'Gigantum AutoCommit', 'email': 'noreply@gigantum.io'}",
                    'labbookName': 'notes-test-2',
                    'level': 'USER_MINOR',
                    'message': 'Added a new file in this test 3',
                    'tags': [
                        'user',
                        'minor'
                    ]
                },
                {
                    'author': "{'name': 'Gigantum AutoCommit', 'email': 'noreply@gigantum.io'}",
                    'labbookName': 'notes-test-2',
                    'level': 'USER_MINOR',
                    'message': 'Added a new file in this test 2',
                    'tags': [
                        'user',
                        'minor'
                    ]
                },
                {
                    'author': "{'name': 'Gigantum AutoCommit', 'email': 'noreply@gigantum.io'}",
                    'labbookName': 'notes-test-2',
                    'level': 'USER_MINOR',
                    'message': 'Added a new file in this test 1',
                    'tags': [
                        'user',
                        'minor'
                    ]
                },
                {
                    'author': "{'name': 'Gigantum AutoCommit', 'email': 'noreply@gigantum.io'}",
                    'labbookName': 'notes-test-2',
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

snapshots['TestNoteService.test_get_note_summaries 1'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 38,
                    'line': 3
                }
            ],
            'message': 'Unknown argument "labbookName" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 4
                }
            ],
            'message': 'Unknown argument "message" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 5
                }
            ],
            'message': 'Unknown argument "level" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 6
                }
            ],
            'message': 'Unknown argument "linkedCommit" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 7
                }
            ],
            'message': 'Unknown argument "tags" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 8
                }
            ],
            'message': 'Unknown argument "freeText" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 9
                }
            ],
            'message': 'Unknown argument "objects" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 31,
                    'line': 11
                }
            ],
            'message': 'Cannot query field "labbookName" on type "Note".'
        },
        {
            'locations': [
                {
                    'column': 33,
                    'line': 18
                }
            ],
            'message': 'Cannot query field "key" on type "NoteObjectConnection".'
        },
        {
            'locations': [
                {
                    'column': 33,
                    'line': 19
                }
            ],
            'message': 'Cannot query field "objectType" on type "NoteObjectConnection".'
        },
        {
            'locations': [
                {
                    'column': 33,
                    'line': 20
                }
            ],
            'message': 'Cannot query field "value" on type "NoteObjectConnection".'
        },
        {
            'locations': [
                {
                    'column': 27,
                    'line': 3
                }
            ],
            'message': 'Field "createNote" argument "input" of type "CreateNoteInput!" is required but not provided.'
        }
    ]
}

snapshots['TestNoteService.test_get_note_summaries 2'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 38,
                    'line': 3
                }
            ],
            'message': 'Unknown argument "labbookName" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 4
                }
            ],
            'message': 'Unknown argument "message" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 5
                }
            ],
            'message': 'Unknown argument "level" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 6
                }
            ],
            'message': 'Unknown argument "linkedCommit" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 7
                }
            ],
            'message': 'Unknown argument "tags" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 8
                }
            ],
            'message': 'Unknown argument "freeText" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 9
                }
            ],
            'message': 'Unknown argument "objects" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 31,
                    'line': 11
                }
            ],
            'message': 'Cannot query field "labbookName" on type "Note".'
        },
        {
            'locations': [
                {
                    'column': 33,
                    'line': 18
                }
            ],
            'message': 'Cannot query field "key" on type "NoteObjectConnection".'
        },
        {
            'locations': [
                {
                    'column': 33,
                    'line': 19
                }
            ],
            'message': 'Cannot query field "objectType" on type "NoteObjectConnection".'
        },
        {
            'locations': [
                {
                    'column': 33,
                    'line': 20
                }
            ],
            'message': 'Cannot query field "value" on type "NoteObjectConnection".'
        },
        {
            'locations': [
                {
                    'column': 27,
                    'line': 3
                }
            ],
            'message': 'Field "createNote" argument "input" of type "CreateNoteInput!" is required but not provided.'
        }
    ]
}

snapshots['TestNoteService.test_get_note_summaries 3'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 38,
                    'line': 3
                }
            ],
            'message': 'Unknown argument "labbookName" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 4
                }
            ],
            'message': 'Unknown argument "message" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 5
                }
            ],
            'message': 'Unknown argument "level" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 6
                }
            ],
            'message': 'Unknown argument "linkedCommit" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 7
                }
            ],
            'message': 'Unknown argument "tags" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 8
                }
            ],
            'message': 'Unknown argument "freeText" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 9
                }
            ],
            'message': 'Unknown argument "objects" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 31,
                    'line': 11
                }
            ],
            'message': 'Cannot query field "labbookName" on type "Note".'
        },
        {
            'locations': [
                {
                    'column': 33,
                    'line': 18
                }
            ],
            'message': 'Cannot query field "key" on type "NoteObjectConnection".'
        },
        {
            'locations': [
                {
                    'column': 33,
                    'line': 19
                }
            ],
            'message': 'Cannot query field "objectType" on type "NoteObjectConnection".'
        },
        {
            'locations': [
                {
                    'column': 33,
                    'line': 20
                }
            ],
            'message': 'Cannot query field "value" on type "NoteObjectConnection".'
        },
        {
            'locations': [
                {
                    'column': 27,
                    'line': 3
                }
            ],
            'message': 'Field "createNote" argument "input" of type "CreateNoteInput!" is required but not provided.'
        }
    ]
}

snapshots['TestNoteService.test_get_note_summaries 4'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 38,
                    'line': 3
                }
            ],
            'message': 'Unknown argument "labbookName" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 4
                }
            ],
            'message': 'Unknown argument "message" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 5
                }
            ],
            'message': 'Unknown argument "level" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 6
                }
            ],
            'message': 'Unknown argument "linkedCommit" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 7
                }
            ],
            'message': 'Unknown argument "tags" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 8
                }
            ],
            'message': 'Unknown argument "freeText" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 9
                }
            ],
            'message': 'Unknown argument "objects" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 31,
                    'line': 11
                }
            ],
            'message': 'Cannot query field "labbookName" on type "Note".'
        },
        {
            'locations': [
                {
                    'column': 33,
                    'line': 18
                }
            ],
            'message': 'Cannot query field "key" on type "NoteObjectConnection".'
        },
        {
            'locations': [
                {
                    'column': 33,
                    'line': 19
                }
            ],
            'message': 'Cannot query field "objectType" on type "NoteObjectConnection".'
        },
        {
            'locations': [
                {
                    'column': 33,
                    'line': 20
                }
            ],
            'message': 'Cannot query field "value" on type "NoteObjectConnection".'
        },
        {
            'locations': [
                {
                    'column': 27,
                    'line': 3
                }
            ],
            'message': 'Field "createNote" argument "input" of type "CreateNoteInput!" is required but not provided.'
        }
    ]
}

snapshots['TestNoteService.test_get_note_summaries 5'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 38,
                    'line': 3
                }
            ],
            'message': 'Unknown argument "labbookName" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 4
                }
            ],
            'message': 'Unknown argument "message" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 5
                }
            ],
            'message': 'Unknown argument "level" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 6
                }
            ],
            'message': 'Unknown argument "linkedCommit" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 7
                }
            ],
            'message': 'Unknown argument "tags" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 8
                }
            ],
            'message': 'Unknown argument "freeText" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 29,
                    'line': 9
                }
            ],
            'message': 'Unknown argument "objects" on field "createNote" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 31,
                    'line': 11
                }
            ],
            'message': 'Cannot query field "labbookName" on type "Note".'
        },
        {
            'locations': [
                {
                    'column': 33,
                    'line': 18
                }
            ],
            'message': 'Cannot query field "key" on type "NoteObjectConnection".'
        },
        {
            'locations': [
                {
                    'column': 33,
                    'line': 19
                }
            ],
            'message': 'Cannot query field "objectType" on type "NoteObjectConnection".'
        },
        {
            'locations': [
                {
                    'column': 33,
                    'line': 20
                }
            ],
            'message': 'Cannot query field "value" on type "NoteObjectConnection".'
        },
        {
            'locations': [
                {
                    'column': 27,
                    'line': 3
                }
            ],
            'message': 'Field "createNote" argument "input" of type "CreateNoteInput!" is required but not provided.'
        }
    ]
}

snapshots['TestNoteService.test_get_note_summaries 6'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 15,
                    'line': 3
                }
            ],
            'message': 'Cannot query field "noteSummaries" on type "Query".'
        }
    ]
}

snapshots['TestNoteService.test_create_note 1'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 19,
                    'line': 3
                }
            ],
            'message': 'Cannot query field "note" on type "Query". Did you mean "node"?'
        }
    ]
}
