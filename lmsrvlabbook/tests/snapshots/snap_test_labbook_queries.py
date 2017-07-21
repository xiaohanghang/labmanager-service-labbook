# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestLabBookServiceQueries.test_list_labbooks 1'] = {
    'data': {
        'localLabbooks': {
            'edges': [
                {
                    'cursor': 'MA==',
                    'node': {
                        'description': 'my first labbook1',
                        'name': 'labbook1'
                    }
                },
                {
                    'cursor': 'MQ==',
                    'node': {
                        'description': 'my first labbook2',
                        'name': 'labbook2'
                    }
                }
            ]
        }
    }
}

snapshots['TestLabBookServiceQueries.test_get_labbook 1'] = {
    'data': {
        'labbook': {
            'activeBranch': {
                'name': 'master'
            },
            'description': 'my first labbook1',
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_get_labbook 2'] = {
    'data': {
        'labbook': {
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_get_multiple 1'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 15,
                    'line': 7
                }
            ],
            'message': 'Cannot query field "users" on type "Query".'
        },
        {
            'locations': [
                {
                    'column': 15,
                    'line': 10
                }
            ],
            'message': 'Cannot query field "labbooks" on type "Query". Did you mean "labbook" or "localLabbooks"?'
        }
    ]
}
