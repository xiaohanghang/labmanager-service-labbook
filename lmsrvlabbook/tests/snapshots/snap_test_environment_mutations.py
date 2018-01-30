# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestEnvironmentMutations.test_build_image[labbook-build1] 1'] = {
    'data': {
        'labbook': {
            'environment': {
                'containerStatus': 'NOT_RUNNING',
                'imageStatus': 'DOES_NOT_EXIST'
            }
        }
    }
}

snapshots['TestEnvironmentMutations.test_build_image[labbook-build1] 2'] = {
    'data': {
        'buildImage': {
            'environment': {
                'containerStatus': 'NOT_RUNNING',
                'imageStatus': 'BUILD_IN_PROGRESS'
            }
        }
    }
}

snapshots['TestEnvironmentMutations.test_build_image[labbook-build1] 3'] = {
    'data': {
        'labbook': {
            'environment': {
                'containerStatus': 'NOT_RUNNING',
                'imageStatus': 'EXISTS'
            }
        }
    }
}

snapshots['TestEnvironmentMutations.test_build_image_no_cache[labbook-build2] 1'] = {
    'data': {
        'labbook': {
            'environment': {
                'containerStatus': 'NOT_RUNNING',
                'imageStatus': 'DOES_NOT_EXIST'
            }
        }
    }
}

snapshots['TestEnvironmentMutations.test_build_image_no_cache[labbook-build2] 2'] = {
    'data': {
        'buildImage': {
            'environment': {
                'containerStatus': 'NOT_RUNNING',
                'imageStatus': 'BUILD_IN_PROGRESS'
            }
        }
    }
}

snapshots['TestEnvironmentMutations.test_build_image_no_cache[labbook-build2] 3'] = {
    'data': {
        'labbook': {
            'environment': {
                'containerStatus': 'NOT_RUNNING',
                'imageStatus': 'EXISTS'
            }
        }
    }
}

snapshots['TestEnvironmentMutations.test_start_stop_container[labbook-build3] 1'] = {
    'data': {
        'labbook': {
            'environment': {
                'containerStatus': 'NOT_RUNNING',
                'imageStatus': 'DOES_NOT_EXIST'
            }
        }
    }
}

snapshots['TestEnvironmentMutations.test_start_stop_container[labbook-build3] 2'] = {
    'data': {
        'buildImage': {
            'environment': {
                'containerStatus': 'NOT_RUNNING',
                'imageStatus': 'BUILD_IN_PROGRESS'
            }
        }
    }
}

snapshots['TestEnvironmentMutations.test_start_stop_container[labbook-build3] 3'] = {
    'data': {
        'labbook': {
            'environment': {
                'containerStatus': 'NOT_RUNNING',
                'imageStatus': 'EXISTS'
            }
        }
    }
}

snapshots['TestEnvironmentMutations.test_start_stop_container[labbook-build3] 4'] = {
    'data': {
        'startContainer': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 11,
                    'line': 3
                }
            ],
            'message': 'No components found for component class: dev_env'
        }
    ]
}
