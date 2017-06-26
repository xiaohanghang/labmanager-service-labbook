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
                'name': 'labbook1',
                'description': 'my first labbook1'
            },
            {
                'name': 'labbook2',
                'description': 'my first labbook2'
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
            'name': 'a-test-labbook',
            'description': 'a different description!'
        },
        'users': [
            {
                'username': 'default'
            },
            {
                'username': 'tester'
            }
        ],
        'labbooks': [
            {
                'name': 'a-test-labbook',
                'description': 'a different description!'
            },
            {
                'name': 'asdf',
                'description': 'fghghfjghgf3454dfs dsfasf f sfsadf asdf asdf sda'
            }
        ]
    }
}

snapshots['test_get_labbook 1'] = {
    'data': {
        'labbook': {
            'name': 'labbook1',
            'description': 'my first labbook1',
            'localBranches': [
                'master'
            ],
            'remoteBranches': [
            ]
        }
    }
}
