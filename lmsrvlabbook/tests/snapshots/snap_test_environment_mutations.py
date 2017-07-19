# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_build_image 1'] = {
    'data': {
        'environment': {
            'containerStatus': 'NOT_RUNNING',
            'imageStatus': 'DOES_NOT_EXIST'
        }
    }
}

snapshots['test_build_image 2'] = {
    'data': {
        'buildImage': {
            'environment': {
                'containerStatus': 'NOT_RUNNING',
                'imageStatus': 'EXISTS'
            }
        }
    }
}

snapshots['test_build_image 3'] = {
    'data': {
        'environment': {
            'containerStatus': 'NOT_RUNNING',
            'imageStatus': 'EXISTS'
        }
    }
}

snapshots['TestLabBookServiceMutations.test_build_image 1'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 15,
                    'line': 3
                }
            ],
            'message': 'Cannot query field "environment" on type "Query".'
        }
    ]
}

snapshots['TestLabBookServiceMutations.test_build_image 2'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 15,
                    'line': 3
                }
            ],
            'message': 'Cannot query field "buildImage" on type "Mutation".'
        }
    ]
}

snapshots['TestLabBookServiceMutations.test_build_image 3'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 15,
                    'line': 3
                }
            ],
            'message': 'Cannot query field "environment" on type "Query".'
        }
    ]
}
