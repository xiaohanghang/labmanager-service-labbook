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
                        'maintainers': None,
                        'name': 'Data Science Quickstart with JupyterLab',
                        'osClass': 'ubuntu',
                        'osRelease': '16.04',
                        'packageManagers': [
                            'apt',
                            'pip3'
                        ],
                        'readme': 'Empty for now',
                        'tags': [
                            'ubuntu',
                            'python3',
                            'jupyterlab'
                        ],
                        'url': None,
                        'version': None
                    }
                },
                {
                    'node': {
                        'componentId': 'ut-jupyterlab-3',
                        'description': 'Unit Test 3',
                        'developmentTools': [
                            'jupyterlab'
                        ],
                        'dockerImageNamespace': 'gigdev',
                        'dockerImageRepository': 'gm-quickstart',
                        'dockerImageServer': 'hub.docker.com',
                        'dockerImageTag': '9718fedc-2018-01-16',
                        'icon': 'data:image/png;base64,<base64 encoded png image>',
                        'id': 'QmFzZUNvbXBvbmVudDpnaWctZGV2X2NvbXBvbmVudHMyJnV0LWp1cHl0ZXJsYWItMyYw',
                        'languages': [
                            'python3'
                        ],
                        'license': 'MIT',
                        'maintainers': None,
                        'name': 'Unit Test 3',
                        'osClass': 'ubuntu',
                        'osRelease': '16.04',
                        'packageManagers': [
                            'apt',
                            'pip3'
                        ],
                        'readme': 'Empty for now',
                        'tags': [
                            'ubuntu',
                            'python3',
                            'jupyterlab'
                        ],
                        'url': None,
                        'version': None
                    }
                },
                {
                    'node': {
                        'componentId': 'ut-jupyterlab-1',
                        'description': 'Unit Test 1',
                        'developmentTools': [
                            'jupyterlab'
                        ],
                        'dockerImageNamespace': 'gigdev',
                        'dockerImageRepository': 'gm-quickstart',
                        'dockerImageServer': 'hub.docker.com',
                        'dockerImageTag': '9718fedc-2018-01-16',
                        'icon': 'data:image/png;base64,<base64 encoded png image>',
                        'id': 'QmFzZUNvbXBvbmVudDpnaWctZGV2X2NvbXBvbmVudHMyJnV0LWp1cHl0ZXJsYWItMSYw',
                        'languages': [
                            'python3'
                        ],
                        'license': 'MIT',
                        'maintainers': None,
                        'name': 'Unit Test1',
                        'osClass': 'ubuntu',
                        'osRelease': '16.04',
                        'packageManagers': [
                            'apt',
                            'pip3'
                        ],
                        'readme': 'Empty for now',
                        'tags': [
                            'ubuntu',
                            'python3',
                            'jupyterlab'
                        ],
                        'url': None,
                        'version': None
                    }
                },
                {
                    'node': {
                        'componentId': 'ut-jupyterlab-2',
                        'description': 'Unit Test 2',
                        'developmentTools': [
                            'jupyterlab'
                        ],
                        'dockerImageNamespace': 'gigdev',
                        'dockerImageRepository': 'gm-quickstart',
                        'dockerImageServer': 'hub.docker.com',
                        'dockerImageTag': '9718fedc-2018-01-16',
                        'icon': 'data:image/png;base64,<base64 encoded png image>',
                        'id': 'QmFzZUNvbXBvbmVudDpnaWctZGV2X2NvbXBvbmVudHMyJnV0LWp1cHl0ZXJsYWItMiYw',
                        'languages': [
                            'python3'
                        ],
                        'license': 'MIT',
                        'maintainers': None,
                        'name': 'Unit Test 2',
                        'osClass': 'ubuntu',
                        'osRelease': '16.04',
                        'packageManagers': [
                            'apt',
                            'pip3'
                        ],
                        'readme': 'Empty for now',
                        'tags': [
                            'ubuntu',
                            'python3',
                            'jupyterlab'
                        ],
                        'url': None,
                        'version': None
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
                        'maintainers': None,
                        'name': 'Data Science Quickstart with JupyterLab',
                        'osClass': 'ubuntu',
                        'osRelease': '16.04',
                        'packageManagers': [
                            'apt',
                            'pip3'
                        ],
                        'readme': 'Empty for now',
                        'tags': [
                            'ubuntu',
                            'python3',
                            'jupyterlab'
                        ],
                        'url': None,
                        'version': None
                    }
                }
            ],
            'pageInfo': {
                'hasNextPage': True
            }
        }
    }
}

snapshots['TestEnvironmentBaseImageQueries.test_get_available_base_images_pagination 2'] = {
    'data': {
        'availableBases': {
            'edges': [
                {
                    'cursor': 'Mg==',
                    'node': {
                        'componentId': 'ut-jupyterlab-1',
                        'description': 'Unit Test 1',
                        'developmentTools': [
                            'jupyterlab'
                        ],
                        'dockerImageNamespace': 'gigdev',
                        'dockerImageRepository': 'gm-quickstart',
                        'dockerImageServer': 'hub.docker.com',
                        'dockerImageTag': '9718fedc-2018-01-16',
                        'icon': 'data:image/png;base64,<base64 encoded png image>',
                        'id': 'QmFzZUNvbXBvbmVudDpnaWctZGV2X2NvbXBvbmVudHMyJnV0LWp1cHl0ZXJsYWItMSYw',
                        'languages': [
                            'python3'
                        ],
                        'license': 'MIT',
                        'maintainers': None,
                        'name': 'Unit Test1',
                        'osClass': 'ubuntu',
                        'osRelease': '16.04',
                        'packageManagers': [
                            'apt',
                            'pip3'
                        ],
                        'readme': 'Empty for now',
                        'tags': [
                            'ubuntu',
                            'python3',
                            'jupyterlab'
                        ],
                        'url': None,
                        'version': None
                    }
                },
                {
                    'cursor': 'Mw==',
                    'node': {
                        'componentId': 'ut-jupyterlab-2',
                        'description': 'Unit Test 2',
                        'developmentTools': [
                            'jupyterlab'
                        ],
                        'dockerImageNamespace': 'gigdev',
                        'dockerImageRepository': 'gm-quickstart',
                        'dockerImageServer': 'hub.docker.com',
                        'dockerImageTag': '9718fedc-2018-01-16',
                        'icon': 'data:image/png;base64,<base64 encoded png image>',
                        'id': 'QmFzZUNvbXBvbmVudDpnaWctZGV2X2NvbXBvbmVudHMyJnV0LWp1cHl0ZXJsYWItMiYw',
                        'languages': [
                            'python3'
                        ],
                        'license': 'MIT',
                        'maintainers': None,
                        'name': 'Unit Test 2',
                        'osClass': 'ubuntu',
                        'osRelease': '16.04',
                        'packageManagers': [
                            'apt',
                            'pip3'
                        ],
                        'readme': 'Empty for now',
                        'tags': [
                            'ubuntu',
                            'python3',
                            'jupyterlab'
                        ],
                        'url': None,
                        'version': None
                    }
                }
            ],
            'pageInfo': {
                'hasNextPage': False
            }
        }
    }
}

snapshots['TestEnvironmentBaseImageQueries.test_get_available_base_images_pagination 3'] = {
    'data': {
        'availableBases': {
            'edges': [
                {
                    'cursor': 'Mg==',
                    'node': {
                        'componentId': 'ut-jupyterlab-1',
                        'description': 'Unit Test 1',
                        'developmentTools': [
                            'jupyterlab'
                        ],
                        'dockerImageNamespace': 'gigdev',
                        'dockerImageRepository': 'gm-quickstart',
                        'dockerImageServer': 'hub.docker.com',
                        'dockerImageTag': '9718fedc-2018-01-16',
                        'icon': 'data:image/png;base64,<base64 encoded png image>',
                        'id': 'QmFzZUNvbXBvbmVudDpnaWctZGV2X2NvbXBvbmVudHMyJnV0LWp1cHl0ZXJsYWItMSYw',
                        'languages': [
                            'python3'
                        ],
                        'license': 'MIT',
                        'maintainers': None,
                        'name': 'Unit Test1',
                        'osClass': 'ubuntu',
                        'osRelease': '16.04',
                        'packageManagers': [
                            'apt',
                            'pip3'
                        ],
                        'readme': 'Empty for now',
                        'tags': [
                            'ubuntu',
                            'python3',
                            'jupyterlab'
                        ],
                        'url': None,
                        'version': None
                    }
                }
            ],
            'pageInfo': {
                'hasNextPage': True
            }
        }
    }
}

snapshots['TestEnvironmentBaseImageQueries.test_get_available_base_images_pagination_reverse 1'] = {
    'data': {
        'availableBases': {
            'edges': [
                {
                    'cursor': 'Mw==',
                    'node': {
                        'componentId': 'ut-jupyterlab-2',
                        'description': 'Unit Test 2',
                        'developmentTools': [
                            'jupyterlab'
                        ],
                        'dockerImageNamespace': 'gigdev',
                        'dockerImageRepository': 'gm-quickstart',
                        'dockerImageServer': 'hub.docker.com',
                        'dockerImageTag': '9718fedc-2018-01-16',
                        'icon': 'data:image/png;base64,<base64 encoded png image>',
                        'id': 'QmFzZUNvbXBvbmVudDpnaWctZGV2X2NvbXBvbmVudHMyJnV0LWp1cHl0ZXJsYWItMiYw',
                        'languages': [
                            'python3'
                        ],
                        'license': 'MIT',
                        'maintainers': None,
                        'name': 'Unit Test 2',
                        'osClass': 'ubuntu',
                        'osRelease': '16.04',
                        'packageManagers': [
                            'apt',
                            'pip3'
                        ],
                        'readme': 'Empty for now',
                        'tags': [
                            'ubuntu',
                            'python3',
                            'jupyterlab'
                        ],
                        'url': None,
                        'version': None
                    }
                }
            ],
            'pageInfo': {
                'hasNextPage': False,
                'hasPreviousPage': True
            }
        }
    }
}

snapshots['TestEnvironmentBaseImageQueries.test_get_available_base_images_pagination_reverse 2'] = {
    'data': {
        'availableBases': {
            'edges': [
                {
                    'cursor': 'MA==',
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
                        'maintainers': None,
                        'name': 'Data Science Quickstart with JupyterLab',
                        'osClass': 'ubuntu',
                        'osRelease': '16.04',
                        'packageManagers': [
                            'apt',
                            'pip3'
                        ],
                        'readme': 'Empty for now',
                        'tags': [
                            'ubuntu',
                            'python3',
                            'jupyterlab'
                        ],
                        'url': None,
                        'version': None
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
            'maintainers': None,
            'name': 'Data Science Quickstart with JupyterLab',
            'osClass': 'ubuntu',
            'osRelease': '16.04',
            'packageManagers': [
                'apt',
                'pip3'
            ],
            'readme': 'Empty for now',
            'tags': [
                'ubuntu',
                'python3',
                'jupyterlab'
            ],
            'url': None,
            'version': None
        }
    }
}
