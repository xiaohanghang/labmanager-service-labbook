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
                'imageStatus': 'EXISTS',
                'containerStatus': 'NOT_RUNNING'
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
