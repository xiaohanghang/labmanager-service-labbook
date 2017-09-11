# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestLabBookServiceQueries.test_query_finished_task 1'] = {
    'data': {
        'jobStatus': {
            'result': '0',
            'status': 'finished'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_query_failed_task 1'] = {
    'data': {
        'jobStatus': {
            'result': None,
            'status': 'failed'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_query_queued_task 1'] = {
    'data': {
        'jobStatus': {
            'result': None,
            'status': 'queued'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_query_started_task 1'] = {
    'data': {
        'jobStatus': {
            'result': None,
            'status': 'started'
        }
    }
}
