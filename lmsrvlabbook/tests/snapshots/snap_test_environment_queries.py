# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestEnvironmentServiceQueries.test_get_environment_status 1'] = {
    'data': {
        'labbook': {
            'environment': {
                'containerStatus': 'NOT_RUNNING',
                'imageStatus': 'DOES_NOT_EXIST'
            }
        }
    }
}

snapshots['TestEnvironmentServiceQueries.test_get_base 1'] = {
    'data': {
        'createLabbook': {
            'labbook': {
                'description': 'my test 1',
                'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2stYmFzZS10ZXN0',
                'name': 'labbook-base-test'
            }
        }
    }
}

snapshots['TestEnvironmentServiceQueries.test_get_base 2'] = {
    'data': {
        'labbook': {
            'description': 'my test 1',
            'environment': {
                'base': {
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
                    'tags': [
                        'ubuntu',
                        'python3',
                        'jupyterlab'
                    ],
                    'url': None
                }
            },
            'name': 'labbook-base-test'
        }
    }
}

snapshots['TestEnvironmentServiceQueries.test_get_custom 1'] = {
    'data': {
        'labbook': {
            'environment': {
                'customDependencies': {
                    'edges': [
                    ],
                    'pageInfo': {
                        'hasNextPage': False,
                        'hasPreviousPage': False
                    }
                }
            }
        }
    }
}

snapshots['TestEnvironmentServiceQueries.test_get_custom 2'] = {
    'data': {
        'labbook': {
            'environment': {
                'customDependencies': {
                    'edges': [
                        {
                            'cursor': 'MA==',
                            'node': {
                                'componentId': 'pillow',
                                'description': 'Pillow v4.2.1 for Ubuntu and Python3',
                                'dockerSnippet': '''RUN apt-get -y install libjpeg-dev libtiff5-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjpeg-dev
RUN pip3 install Pillow==4.2.1 
''',
                                'id': 'Q3VzdG9tQ29tcG9uZW50OmdpZy1kZXZfY29tcG9uZW50czImcGlsbG93JjA=',
                                'license': None,
                                'name': 'Pillow',
                                'repository': 'gig-dev_components2',
                                'requiredPackageManagers': None,
                                'revision': 0,
                                'tags': [
                                    'ubuntu',
                                    'python',
                                    'python3',
                                    'image',
                                    'jpeg',
                                    'png'
                                ],
                                'url': None
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
    }
}

snapshots['TestEnvironmentServiceQueries.test_get_package_manager 1'] = {
    'data': {
        'labbook': {
            'environment': {
                'packageDependencies': {
                    'edges': [
                    ],
                    'pageInfo': {
                        'hasNextPage': False
                    }
                }
            }
        }
    }
}
