# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_list_users 1'] = {
    'data': {
        'users': [
            {
                'username': 'test1'
            },
            {
                'username': 'test2'
            },
            {
                'username': 'test3'
            }
        ]
    }
}

snapshots['test_list_labbooks 1'] = {
    'data': {
        'labbooks': [
            {
                'description': 'my first labbook1',
                'name': 'labbook1'
            },
            {
                'description': 'my first labbook2',
                'name': 'labbook2'
            }
        ]
    }
}

snapshots['test_get_labbook 2'] = {
    'data': {
        'labbook': {
            'name': 'labbook1'
        }
    }
}

snapshots['test_get_multiple 1'] = {
    'data': {
        'labbook': {
            'description': 'a different description!',
            'name': 'a-test-labbook'
        },
        'labbooks': [
            {
                'description': 'a different description!',
                'name': 'a-test-labbook'
            },
            {
                'description': 'fghghfjghgf3454dfs dsfasf f sfsadf asdf asdf sda',
                'name': 'asdf'
            }
        ],
        'users': [
            {
                'username': 'default'
            },
            {
                'username': 'tester'
            }
        ]
    }
}

snapshots['test_get_labbook 1'] = {
    'data': {
        'labbook': {
            'description': 'my first labbook1',
            'localBranches': [
                'master'
            ],
            'name': 'labbook1',
            'remoteBranches': [
            ]
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_users 1'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 15,
                    'line': 3
                }
            ],
            'message': 'Cannot query field "users" on type "Query".'
        }
    ]
}

snapshots['TestLabBookServiceQueries.test_list_labbooks 1'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 15,
                    'line': 3
                }
            ],
            'message': 'Cannot query field "labbooks" on type "Query". Did you mean "labbook" or "localLabbooks"?'
        }
    ]
}
