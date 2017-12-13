# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestNodeQueries.test_node_labbook_from_object 1'] = {
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

snapshots['TestNodeQueries.test_node_labbook_from_mutation 1'] = {
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

snapshots['TestNodeQueries.test_node_environment 1'] = {
    'data': {
        'node': {
            'description': 'Example labbook by mutation.',
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

snapshots['TestNodeQueries.test_node_environment 2'] = {
    'data': {
        'node': {
            'containerStatus': 'NOT_RUNNING',
            'id': 'RW52aXJvbm1lbnQ6ZGVmYXVsdCZkZWZhdWx0Jm5vZGUtZW52LXRlc3QtbGI=',
            'imageStatus': 'DOES_NOT_EXIST'
        }
    }
}

snapshots['TestNodeQueries.test_favorites_node 1'] = {
    'data': {
        'node': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 29,
                    'line': 3
                }
            ],
            'message': 'Invalid favorite index value'
        }
    ]
}

snapshots['TestNodeQueries.test_favorites_node 2'] = {
    'data': {
        'node': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 29,
                    'line': 3
                }
            ],
            'message': 'Invalid favorite index value'
        }
    ]
}

snapshots['TestNodeQueries.test_favorites_node 3'] = {
    'data': {
        'node': {
            'description': 'My file with stuff 1',
            'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSYw',
            'index': 0,
            'isDir': False,
            'key': 'test1.txt'
        }
    }
}

snapshots['TestNodeQueries.test_file_node 1'] = {
    'data': {
        'node': {
            'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnRlc3QxLnR4dA==',
            'isDir': False,
            'key': 'test1.txt',
            'size': 5
        }
    }
}
