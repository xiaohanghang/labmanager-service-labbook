# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestLabBookServiceMutations.test_build_image 1'] = {
    'data': {
        'localLabbooks': {
            'edges': [
                {
                    'node': {
                        'description': 'building an env',
                        'id': 'TGFiYm9va1N1bW1hcnk6ZGVmYXVsdCZsYWJib29rLWJ1aWxk',
                        'name': 'labbook-build'
                    }
                }
            ]
        }
    }
}

snapshots['TestLabBookServiceMutations.test_build_image 2'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 26,
                    'line': 3
                }
            ],
            'message': 'Unknown argument "labbookName" on field "buildImage" of type "Mutation".'
        },
        {
            'locations': [
                {
                    'column': 15,
                    'line': 3
                }
            ],
            'message': 'Field "buildImage" argument "input" of type "BuildImageInput!" is required but not provided.'
        }
    ]
}

snapshots['TestLabBookServiceMutations.test_build_image 3'] = {
    'data': {
        'labbook': {
            'environment': {
                'containerStatus': 'NOT_RUNNING',
                'imageStatus': 'DOES_NOT_EXIST'
            }
        }
    }
}
