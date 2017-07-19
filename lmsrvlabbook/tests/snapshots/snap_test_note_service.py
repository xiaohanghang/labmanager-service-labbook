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
