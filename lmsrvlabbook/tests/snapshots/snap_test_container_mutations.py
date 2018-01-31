# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestContainerMutations.test_start_stop_container 1'] = {
    'data': {
        'labbook': {
            'environment': {
                'containerStatus': 'NOT_RUNNING',
                'imageStatus': 'DOES_NOT_EXIST'
            }
        }
    }
}

snapshots['TestContainerMutations.test_start_stop_container 2'] = {
    'data': {
        'startContainer': {
            'environment': {
                'containerStatus': 'NOT_RUNNING',
                'imageStatus': 'DOES_NOT_EXIST'
            }
        }
    }
}
