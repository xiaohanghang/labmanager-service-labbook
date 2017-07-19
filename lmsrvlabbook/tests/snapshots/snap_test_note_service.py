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
                    'column': 35,
                    'line': 12
                }
            ],
            'message': 'Cannot query field "labbookName" on type "Note".'
        }
    ]
}

snapshots['TestNoteService.test_get_note_summaries 2'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 35,
                    'line': 12
                }
            ],
            'message': 'Cannot query field "labbookName" on type "Note".'
        }
    ]
}

snapshots['TestNoteService.test_get_note_summaries 3'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 35,
                    'line': 12
                }
            ],
            'message': 'Cannot query field "labbookName" on type "Note".'
        }
    ]
}

snapshots['TestNoteService.test_get_note_summaries 4'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 35,
                    'line': 12
                }
            ],
            'message': 'Cannot query field "labbookName" on type "Note".'
        }
    ]
}

snapshots['TestNoteService.test_get_note_summaries 5'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 35,
                    'line': 12
                }
            ],
            'message': 'Cannot query field "labbookName" on type "Note".'
        }
    ]
}

snapshots['TestNoteService.test_get_note_summaries 6'] = {
    'data': {
        'labbook': {
            'notes': None
        }
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 4
                }
            ],
            'message': 'Commit e8be95706000d48df2857c3b2d58c8de037ee838 not found'
        }
    ]
}
