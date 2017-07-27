# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestLabBookServiceQueries.test_node_labbook_from_object 1'] = {
    'data': {
        'node': {
            'activeBranch': {
                'name': 'master'
            },
            'description': 'Test cat labbook from obj',
            'id': 'TGFiYm9vazpkZWZhdWx0JmNhdC1sYWItYm9vazE=',
            'name': 'cat-lab-book1'
        }
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

snapshots['TestLabBookServiceQueries.test_node_environment 1'] = {
    'data': {
        'node': {
            'description': 'Node env test labbook.',
            'environment': {
                'containerStatus': 'NOT_RUNNING',
                'id': 'RW52aXJvbm1lbnQ6ZGVmYXVsdCZkZWZhdWx0Jm5vZGUtZW52LXRlc3QtbGI=',
                'imageStatus': 'DOES_NOT_EXIST'
            },
            'id': 'TGFiYm9vazpkZWZhdWx0Jm5vZGUtZW52LXRlc3QtbGI=',
            'name': 'node-env-test-lb'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_node_environment 2'] = {
    'data': {
        'node': {
            'containerStatus': 'NOT_RUNNING',
            'id': 'RW52aXJvbm1lbnQ6ZGVmYXVsdCZkZWZhdWx0Jm5vZGUtZW52LXRlc3QtbGI=',
            'imageStatus': 'DOES_NOT_EXIST'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_node_notes 1'] = {
    'data': {
        'node': None
    }
}
