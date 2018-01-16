# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestEnvironmentBaseImageQueries.test_get_available_base_images 1'] = {
    'data': {
        'availableBases': {
            'edges': [
                {
                    'node': {
                        'componentId': 'quickstart-jupyterlab',
                        'description': 'Data Science Quickstart using Jupyterlab, numpy, and Matplotlib. A great base for any analysis.',
                        'developmentTools': [
                            'jupyterlab'
                        ],
                        'dockerImageNamespace': 'gigdev',
                        'dockerImageRepository': 'gm-quickstart',
                        'dockerImageServer': 'hub.docker.com',
                        'dockerImageTag': '9718fedc-2018-01-16',
                        'icon': 'data:image/png;base64,<base64 encoded png image>',
                        'id': 'QmFzZUNvbXBvbmVudDpnaWctZGV2X2NvbXBvbmVudHMyJnF1aWNrc3RhcnQtanVweXRlcmxhYiYx',
                        'languages': [
                            'python3'
                        ],
                        'license': 'MIT',
                        'name': 'Data Science Quickstart with JupyterLab',
                        'osClass': 'ubuntu',
                        'osRelease': '16.04',
                        'packageManagers': [
                            'apt',
                            'pip3'
                        ],
                        'readme': 'Empty for now',
                        'repository': 'gig-dev_components2',
                        'revision': 1,
                        'tags': [
                            'ubuntu',
                            'python3',
                            'jupyterlab'
                        ],
                        'url': None
                    }
                }
            ]
        }
    }
}

snapshots['TestEnvironmentBaseImageQueries.test_get_available_base_images_pagination 1'] = {
    'data': {
        'availableBases': {
            'edges': [
                {
                    'cursor': 'MA==',
                    'node': {
                        'id': 'QmFzZUNvbXBvbmVudDpnaWctZGV2X2NvbXBvbmVudHMyJnF1aWNrc3RhcnQtanVweXRlcmxhYiYx',
                        'name': 'Data Science Quickstart with JupyterLab'
                    }
                }
            ],
            'pageInfo': {
                'hasNextPage': False
            }
        }
    }
}

snapshots['TestEnvironmentBaseImageQueries.test_get_available_base_images_pagination 2'] = {
    'data': {
        'availableBases': {
            'edges': [
            ],
            'pageInfo': {
                'hasNextPage': False
            }
        }
    }
}

snapshots['TestEnvironmentBaseImageQueries.test_get_available_base_images_pagination_reverse 1'] = {
    'data': {
        'availableBases': {
            'edges': [
                {
                    'cursor': 'MA==',
                    'node': {
                        'id': 'QmFzZUNvbXBvbmVudDpnaWctZGV2X2NvbXBvbmVudHMyJnF1aWNrc3RhcnQtanVweXRlcmxhYiYx',
                        'name': 'Data Science Quickstart with JupyterLab'
                    }
                }
            ],
            'pageInfo': {
                'hasNextPage': False,
                'hasPreviousPage': False
            }
        }
    }
}

snapshots['TestEnvironmentBaseImageQueries.test_get_base_image_by_node 1'] = {
    'data': {
        'node': {
            'componentId': 'quickstart-jupyterlab',
            'description': 'Data Science Quickstart using Jupyterlab, numpy, and Matplotlib. A great base for any analysis.',
            'developmentTools': [
                'jupyterlab'
            ],
            'dockerImageNamespace': 'gigdev',
            'dockerImageRepository': 'gm-quickstart',
            'dockerImageServer': 'hub.docker.com',
            'dockerImageTag': '9718fedc-2018-01-16',
            'icon': 'data:image/png;base64,<base64 encoded png image>',
            'id': 'QmFzZUNvbXBvbmVudDpnaWctZGV2X2NvbXBvbmVudHMyJnF1aWNrc3RhcnQtanVweXRlcmxhYiYx',
            'languages': [
                'python3'
            ],
            'license': 'MIT',
            'name': 'Data Science Quickstart with JupyterLab',
            'osClass': 'ubuntu',
            'osRelease': '16.04',
            'packageManagers': [
                'apt',
                'pip3'
            ],
            'readme': 'Empty for now',
            'repository': 'gig-dev_components2',
            'revision': 1,
            'tags': [
                'ubuntu',
                'python3',
                'jupyterlab'
            ],
            'url': None
        }
    }
}
