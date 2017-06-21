# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_create_labbook 1'] = {
    'data': {
        'labbook': {
            'name': 'test-lab-book',
            'description': 'my test description'
        }
    }
}

snapshots['test_create_labbook_already_exists 1'] = {
    'data': {
        'createLabbook': {
            'labbook': {
                'name': 'test-lab-book',
                'description': 'my test description'
            }
        }
    }
}

snapshots['test_create_labbook_already_exists 2'] = {
    'errors': [
        {
            'message': 'LabBook `test-lab-book` already exists locally. Choose a new LabBook name',
            'locations': [
                {
                    'line': 3,
                    'column': 15
                }
            ]
        }
    ],
    'data': {
        'createLabbook': None
    }
}
