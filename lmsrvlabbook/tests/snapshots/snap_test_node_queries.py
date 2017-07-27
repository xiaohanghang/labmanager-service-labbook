# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestLabBookServiceQueries.test_node_labbook 1'] = {
    'data': {
        'node': {
            'activeBranch': {
                'name': 'master'
            },
            'description': 'my test description',
            'id': 'TGFiYm9vazpkZWZhdWx0JnRlc3QtbGFiLWJvb2sx',
            'name': 'test-lab-book1'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_node_labbook_from_object 1'] = {
    'data': {
        'node': None
    }
}

snapshots['TestLabBookServiceQueries.test_node_labbook_from_mutation 1'] = {
    'data': {
        'node': {
            'activeBranch': {
                'name': 'master'
            },
            'description': 'my test description',
            'id': 'TGFiYm9vazpkZWZhdWx0JnRlc3QtbGFiLWJvb2sx',
            'name': 'test-lab-book1'
        }
    }
}
