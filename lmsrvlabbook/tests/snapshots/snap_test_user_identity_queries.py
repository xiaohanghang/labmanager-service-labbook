# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestUserIdentityQueries.test_logged_in_user 1'] = {
    'data': {
        'userIdentity': {
            'email': 'jane@doe.com',
            'familyName': 'Doe',
            'givenName': 'Jane',
            'id': 'VXNlcklkZW50aXR5OmRlZmF1bHQ=',
            'username': 'default'
        }
    }
}

snapshots['TestUserIdentityQueries.test_no_logged_in_user 1'] = {
    'data': {
        'userIdentity': {
            'email': None,
            'familyName': None,
            'givenName': None,
            'id': 'VXNlcklkZW50aXR5Ok5vbmU=',
            'username': None
        }
    }
}
