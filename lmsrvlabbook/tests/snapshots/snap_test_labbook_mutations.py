# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestLabBookServiceMutations.test_create_labbook 1'] = {
    'data': {
        'labbook': {
            'description': 'my test description',
            'name': 'test-lab-book1'
        }
    }
}

snapshots['TestLabBookServiceMutations.test_create_labbook_already_exists 1'] = {
    'data': {
        'createLabbook': {
            'labbook': {
                'description': 'my test description',
                'name': 'test-lab-book'
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_create_labbook_already_exists 2'] = {
    'data': {
        'createLabbook': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 15,
                    'line': 3
                }
            ],
            'message': 'LabBook `test-lab-book` already exists locally. Choose a new LabBook name'
        }
    ]
}

snapshots['TestLabBookServiceMutations.test_create_branch 1'] = {
    'data': {
        'labbook': {
            'activeBranch': {
                'name': 'master'
            },
            'branches': {
                'edges': [
                    {
                        'node': {
                            'name': 'dev-branch-1'
                        }
                    },
                    {
                        'node': {
                            'name': 'master'
                        }
                    }
                ]
            },
            'description': 'Yada yada blah blah blah 99',
            'name': 'test-lab-book2'
        }
    }
}

snapshots['TestLabBookServiceMutations.test_checkout_branch 1'] = {
    'data': {
        'createBranch': {
            'branch': {
                'name': 'dev-branch-5'
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_checkout_branch 2'] = {
    'data': {
        'labbook': {
            'activeBranch': {
                'name': 'master'
            },
            'branches': {
                'edges': [
                    {
                        'node': {
                            'name': 'dev-branch-5',
                            'prefix': None
                        }
                    },
                    {
                        'node': {
                            'name': 'master',
                            'prefix': None
                        }
                    }
                ]
            },
            'description': 'a different description',
            'name': 'test-lab-book3'
        }
    }
}

snapshots['TestLabBookServiceMutations.test_checkout_branch 3'] = {
    'data': {
        'labbook': {
            'activeBranch': {
                'name': 'dev-branch-5',
                'prefix': None
            },
            'description': 'a different description',
            'name': 'test-lab-book3'
        }
    }
}
