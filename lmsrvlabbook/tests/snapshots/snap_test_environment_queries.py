# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_get_environment_status 1'] = {
    'data': {
        'environment': {
            'containerStatus': 'NOT_RUNNING',
            'imageStatus': 'DOES_NOT_EXIST'
        }
    }
}

snapshots['TestEnvironmentServiceQueries.test_get_environment_status 1'] = {
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
