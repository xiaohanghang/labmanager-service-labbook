# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_create_labbook 1'] = {
    'data': {
        'labbook': {
            'name': 'test-lab-book1',
            'description': 'my test description',
            'owner': {
                'username': 'test_user'
            }
        }
    }
}

snapshots['test_create_labbook_already_exists 1'] = {
    'data': {
        'createLabbook': {
            'labbook': {
                'name': 'test-lab-book',
                'description': 'my test description'
            }
        }
    }
}

snapshots['test_create_labbook_already_exists 2'] = {
    'errors': [
        {
            'message': 'LabBook `test-lab-book` already exists locally. Choose a new LabBook name',
            'locations': [
                {
                    'line': 3,
                    'column': 15
                }
            ]
        }
    ],
    'data': {
        'createLabbook': None
    }
}

snapshots['test_create_branch 1'] = {
    'data': {
        'labbook': {
            'name': 'test-lab-book2',
            'description': 'my test description blah blah 12345',
            'localBranches': [
                'dev-branch-1',
                'master'
            ]
        }
    }
}

snapshots['test_checkout_branch 1'] = {
    'data': {
        'labbook': {
            'name': 'test-lab-book3',
            'description': 'a different description',
            'localBranches': [
                'dev-branch-5',
                'master'
            ],
            'activeBranch': {
                'name': 'master',
                'prefix': 'refs/heads'
            }
        }
    }
}

snapshots['test_checkout_branch 2'] = {
    'data': {
        'labbook': {
            'name': 'test-lab-book3',
            'description': 'a different description',
            'localBranches': [
                'dev-branch-5',
                'master'
            ],
            'activeBranch': {
                'name': 'dev-branch-5',
                'prefix': 'refs/heads'
            }
        }
    }
}
