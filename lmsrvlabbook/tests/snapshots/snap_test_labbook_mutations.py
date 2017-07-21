# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestLabBookServiceMutations.test_create_labbook 1'] = {
    'data': {
        'labbook': {
            'description': 'my test description',
            'name': 'test-lab-book1'
        }
    }
}

snapshots['TestLabBookServiceMutations.test_create_labbook_already_exists 1'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 29,
                    'line': 3
                }
            ],
            'message': 'Unknown argument "name" on field "createLabbook" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 42,
                    'line': 3
                }
            ],
            'message': 'Unknown argument "description" on field "createLabbook" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 15,
                    'line': 3
                }
            ],
            'message': 'Field "createLabbook" argument "input" of type "CreateLabbookInput!" is required but not provided.'
        }
    ]
}

snapshots['TestLabBookServiceMutations.test_create_labbook_already_exists 2'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 29,
                    'line': 3
                }
            ],
            'message': 'Unknown argument "name" on field "createLabbook" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 42,
                    'line': 3
                }
            ],
            'message': 'Unknown argument "description" on field "createLabbook" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 15,
                    'line': 3
                }
            ],
            'message': 'Field "createLabbook" argument "input" of type "CreateLabbookInput!" is required but not provided.'
        }
    ]
}

snapshots['TestLabBookServiceMutations.test_create_branch 1'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 6
                }
            ],
            'message': 'Cannot query field "localBranches" on type "Labbook". Did you mean "branches"?'
        }
    ]
}

snapshots['TestLabBookServiceMutations.test_checkout_branch 1'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 6
                }
            ],
            'message': 'Cannot query field "localBranches" on type "Labbook". Did you mean "branches"?'
        }
    ]
}

snapshots['TestLabBookServiceMutations.test_checkout_branch 2'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 6
                }
            ],
            'message': 'Cannot query field "localBranches" on type "Labbook". Did you mean "branches"?'
        }
    ]
}
