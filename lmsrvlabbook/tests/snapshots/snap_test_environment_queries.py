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

snapshots['TestEnvironmentServiceQueries.test_get_base_image 1'] = {
    'data': {
        'labbook': {
            'environment': {
                'baseImage': None
            }
        }
    }
}

snapshots['TestEnvironmentServiceQueries.test_get_base_image 2'] = {
    'data': {
        'labbook': {
            'environment': {
                'baseImage': {
                    'author': {
                        'organization': 'Aperture Science'
                    },
                    'availablePackageManagers': [
                        'pip3',
                        'apt-get'
                    ],
                    'component': {
                        'componentClass': 'base_image',
                        'name': 'ubuntu1604-python3',
                        'namespace': 'gigantum',
                        'repository': 'gig-dev_environment-components',
                        'version': '0.4'
                    },
                    'id': 'QmFzZUltYWdlOmJhc2VfaW1hZ2UmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dTE2MDQtcHl0aG9uMyYwLjQ=',
                    'info': {
                        'humanName': 'Ubuntu 16.04 Python 3 Developer',
                        'name': 'ubuntu1604-python3',
                        'versionMajor': 0,
                        'versionMinor': 4
                    },
                    'server': 'hub.docker.com',
                    'tag': '7a7c9d41-2017-08-03'
                }
            }
        }
    }
}

snapshots['TestEnvironmentServiceQueries.test_get_dev_env 1'] = {
    'data': {
        'labbook': {
            'environment': {
                'devEnvs': {
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

snapshots['TestEnvironmentServiceQueries.test_get_dev_env 2'] = {
    'data': {
        'labbook': {
            'environment': {
                'devEnvs': {
                    'edges': [
                        {
                            'cursor': 'MA==',
                            'node': {
                                'author': {
                                    'organization': 'Strange Science Laboratories'
                                },
                                'component': {
                                    'componentClass': 'dev_env',
                                    'name': 'jupyter-ubuntu',
                                    'namespace': 'gigantum',
                                    'repository': 'gig-dev_environment-components',
                                    'version': '0.1'
                                },
                                'developmentEnvironmentClass': 'web',
                                'execCommands': [
                                    "jupyter notebook --ip=0.0.0.0 --NotebookApp.token='' --no-browser"
                                ],
                                'exposedTcpPorts': [
                                    '8000',
                                    '8888'
                                ],
                                'id': 'RGV2RW52OmRldl9lbnYmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJmp1cHl0ZXItdWJ1bnR1JjAuMQ==',
                                'info': {
                                    'humanName': 'Python 3 Jupyter Notebook for Ubuntu',
                                    'name': 'jupyter-ubuntu',
                                    'versionMajor': 0,
                                    'versionMinor': 1
                                },
                                'installCommands': [
                                    'pip3 install jupyter'
                                ],
                                'osBaseClass': 'ubuntu'
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

snapshots['TestEnvironmentServiceQueries.test_get_custom 1'] = {
    'data': {
        'labbook': {
            'environment': {
                'customDependencies': {
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

snapshots['TestEnvironmentServiceQueries.test_get_custom 2'] = {
    'data': {
        'labbook': {
            'environment': {
                'customDependencies': {
                    'edges': [
                        {
                            'cursor': 'MA==',
                            'node': {
                                'author': {
                                    'organization': 'Aperture Science'
                                },
                                'component': {
                                    'componentClass': 'custom',
                                    'name': 'ubuntu-python3-pillow',
                                    'namespace': 'gigantum',
                                    'repository': 'gig-dev_environment-components',
                                    'version': '0.3'
                                },
                                'docker': '''RUN apt-get -y install libjpeg-dev libtiff5-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjpeg-dev
RUN pip3 install Pillow==4.2.1 
''',
                                'id': 'Q3VzdG9tRGVwZW5kZW5jeTpjdXN0b20mZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dS1weXRob24zLXBpbGxvdyYwLjM=',
                                'info': {
                                    'humanName': 'Pillow',
                                    'name': 'ubuntu-python3-pillow',
                                    'versionMajor': 0,
                                    'versionMinor': 3
                                },
                                'osBaseClass': 'ubuntu'
                            }
                        }
                    ],
                    'pageInfo': {
                        'hasNextPage': False
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
                'packageManagerDependencies': {
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

snapshots['TestEnvironmentServiceQueries.test_get_package_manager 2'] = {
    'data': {
        'labbook': {
            'environment': {
                'packageManagerDependencies': {
                    'edges': [
                        {
                            'cursor': 'MA==',
                            'node': {
                                'id': 'UGFja2FnZU1hbmFnZXI6cGFja2FnZV9tYW5hZ2VyJmFwdC1nZXQmZG9ja2Vy',
                                'packageManager': 'apt-get',
                                'packageName': 'docker',
                                'packageVersion': None
                            }
                        }
                    ],
                    'pageInfo': {
                        'hasNextPage': True
                    }
                }
            }
        }
    }
}

snapshots['TestEnvironmentServiceQueries.test_get_package_manager 3'] = {
    'data': {
        'labbook': {
            'environment': {
                'packageManagerDependencies': {
                    'edges': [
                        {
                            'cursor': 'MQ==',
                            'node': {
                                'id': 'UGFja2FnZU1hbmFnZXI6cGFja2FnZV9tYW5hZ2VyJmFwdC1nZXQmbHhtbA==',
                                'packageManager': 'apt-get',
                                'packageName': 'lxml',
                                'packageVersion': None
                            }
                        },
                        {
                            'cursor': 'Mg==',
                            'node': {
                                'id': 'UGFja2FnZU1hbmFnZXI6cGFja2FnZV9tYW5hZ2VyJnBpcDMmbnVtcHk=',
                                'packageManager': 'pip3',
                                'packageName': 'numpy',
                                'packageVersion': '1.12'
                            }
                        },
                        {
                            'cursor': 'Mw==',
                            'node': {
                                'id': 'UGFja2FnZU1hbmFnZXI6cGFja2FnZV9tYW5hZ2VyJnBpcDMmcmVxdWVzdHM=',
                                'packageManager': 'pip3',
                                'packageName': 'requests',
                                'packageVersion': None
                            }
                        }
                    ],
                    'pageInfo': {
                        'hasNextPage': False
                    }
                }
            }
        }
    }
}
