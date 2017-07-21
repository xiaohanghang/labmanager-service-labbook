# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestLabBookServiceMutations.test_build_image 1'] = {
    'data': {
        'labbook': {
            'environment': {
                'containerStatus': 'NOT_RUNNING',
                'imageStatus': 'DOES_NOT_EXIST'
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_build_image 2'] = {
    'data': {
        'buildImage': {
            'environment': {
                'containerStatus': 'NOT_RUNNING',
                'imageStatus': 'EXISTS'
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_build_image 3'] = {
    'data': {
        'labbook': {
            'environment': {
                'containerStatus': 'NOT_RUNNING',
                'imageStatus': 'EXISTS'
            }
        }
    }
}
