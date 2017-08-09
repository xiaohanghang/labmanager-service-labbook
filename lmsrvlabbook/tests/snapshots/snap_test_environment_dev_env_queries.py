# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestEnvironmentDevEnvQueries.test_get_available_dev_envs 1'] = {
    'data': {
        'availableDevEnvs': {
            'edges': [
                {
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
                },
                {
                    'node': {
                        'author': {
                            'organization': 'Strange Science Laboratories'
                        },
                        'component': {
                            'componentClass': 'dev_env',
                            'name': 'jupyter-ubuntu-dup',
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
                        'id': 'RGV2RW52OmRldl9lbnYmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJmp1cHl0ZXItdWJ1bnR1LWR1cCYwLjE=',
                        'info': {
                            'humanName': 'Python 3 Jupyter Notebook for Ubuntu',
                            'name': 'jupyter-ubuntu-dup',
                            'versionMajor': 0,
                            'versionMinor': 1
                        },
                        'installCommands': [
                            'pip3 install jupyter'
                        ],
                        'osBaseClass': 'ubuntu'
                    }
                },
                {
                    'node': {
                        'author': {
                            'organization': 'Strange Science Laboratories'
                        },
                        'component': {
                            'componentClass': 'dev_env',
                            'name': 'jupyter-ubuntu',
                            'namespace': 'gigantum-dev',
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
                        'id': 'RGV2RW52OmRldl9lbnYmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtLWRldiZqdXB5dGVyLXVidW50dSYwLjE=',
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
            ]
        }
    }
}

snapshots['TestEnvironmentDevEnvQueries.test_get_available_dev_envs_pagination 1'] = {
    'data': {
        'availableDevEnvs': {
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
                'hasNextPage': True
            }
        }
    }
}

snapshots['TestEnvironmentDevEnvQueries.test_get_available_dev_envs_pagination 2'] = {
    'data': {
        'availableDevEnvs': {
            'edges': [
                {
                    'node': {
                        'author': {
                            'organization': 'Strange Science Laboratories'
                        },
                        'component': {
                            'componentClass': 'dev_env',
                            'name': 'jupyter-ubuntu-dup',
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
                        'id': 'RGV2RW52OmRldl9lbnYmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJmp1cHl0ZXItdWJ1bnR1LWR1cCYwLjE=',
                        'info': {
                            'humanName': 'Python 3 Jupyter Notebook for Ubuntu',
                            'name': 'jupyter-ubuntu-dup',
                            'versionMajor': 0,
                            'versionMinor': 1
                        },
                        'installCommands': [
                            'pip3 install jupyter'
                        ],
                        'osBaseClass': 'ubuntu'
                    }
                },
                {
                    'node': {
                        'author': {
                            'organization': 'Strange Science Laboratories'
                        },
                        'component': {
                            'componentClass': 'dev_env',
                            'name': 'jupyter-ubuntu',
                            'namespace': 'gigantum-dev',
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
                        'id': 'RGV2RW52OmRldl9lbnYmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtLWRldiZqdXB5dGVyLXVidW50dSYwLjE=',
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
                'hasNextPage': False
            }
        }
    }
}

snapshots['TestEnvironmentDevEnvQueries.test_get_available_dev_envs_pagination_reverse 1'] = {
    'data': {
        'availableDevEnvs': {
            'edges': [
                {
                    'node': {
                        'author': {
                            'organization': 'Strange Science Laboratories'
                        },
                        'component': {
                            'componentClass': 'dev_env',
                            'name': 'jupyter-ubuntu',
                            'namespace': 'gigantum-dev',
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
                        'id': 'RGV2RW52OmRldl9lbnYmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtLWRldiZqdXB5dGVyLXVidW50dSYwLjE=',
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
                'hasPreviousPage': True
            }
        }
    }
}

snapshots['TestEnvironmentDevEnvQueries.test_get_available_dev_envs_pagination_reverse 2'] = {
    'data': {
        'availableDevEnvs': {
            'edges': [
                {
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
                },
                {
                    'node': {
                        'author': {
                            'organization': 'Strange Science Laboratories'
                        },
                        'component': {
                            'componentClass': 'dev_env',
                            'name': 'jupyter-ubuntu-dup',
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
                        'id': 'RGV2RW52OmRldl9lbnYmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJmp1cHl0ZXItdWJ1bnR1LWR1cCYwLjE=',
                        'info': {
                            'humanName': 'Python 3 Jupyter Notebook for Ubuntu',
                            'name': 'jupyter-ubuntu-dup',
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

snapshots['TestEnvironmentDevEnvQueries.test_get_dev_env_by_node 1'] = {
    'data': {
        'node': {
            'component': {
                'componentClass': 'dev_env',
                'name': 'jupyter-ubuntu',
                'namespace': 'gigantum-dev',
                'repository': 'gig-dev_environment-components',
                'version': '0.1'
            },
            'info': {
                'humanName': 'Python 3 Jupyter Notebook for Ubuntu',
                'name': 'jupyter-ubuntu',
                'versionMajor': 0,
                'versionMinor': 1
            }
        }
    }
}

snapshots['TestEnvironmentDevEnvQueries.test_get_available_dev_env_versions 1'] = {
    'data': {
        'availableDevEnvVersions': {
            'edges': [
                {
                    'node': {
                        'id': 'RGV2RW52OmRldl9lbnYmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJmp1cHl0ZXItdWJ1bnR1JjAuMQ==',
                        'info': {
                            'humanName': 'Python 3 Jupyter Notebook for Ubuntu',
                            'name': 'jupyter-ubuntu',
                            'versionMajor': 0,
                            'versionMinor': 1
                        }
                    }
                },
                {
                    'node': {
                        'id': 'RGV2RW52OmRldl9lbnYmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJmp1cHl0ZXItdWJ1bnR1JjAuMA==',
                        'info': {
                            'humanName': 'Python 3 Jupyter Notebook for Ubuntu',
                            'name': 'jupyter-ubuntu',
                            'versionMajor': 0,
                            'versionMinor': 0
                        }
                    }
                }
            ]
        }
    }
}

snapshots['TestEnvironmentDevEnvQueries.test_get_available_dev_env_versions_pagination 1'] = {
    'data': {
        'availableDevEnvVersions': {
            'edges': [
                {
                    'cursor': 'MA==',
                    'node': {
                        'id': 'RGV2RW52OmRldl9lbnYmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJmp1cHl0ZXItdWJ1bnR1JjAuMQ==',
                        'info': {
                            'humanName': 'Python 3 Jupyter Notebook for Ubuntu',
                            'name': 'jupyter-ubuntu',
                            'versionMajor': 0,
                            'versionMinor': 1
                        }
                    }
                }
            ],
            'pageInfo': {
                'hasNextPage': True,
                'hasPreviousPage': False
            }
        }
    }
}

snapshots['TestEnvironmentDevEnvQueries.test_get_available_dev_env_versions_pagination 2'] = {
    'data': {
        'availableDevEnvVersions': {
            'edges': [
                {
                    'cursor': 'MQ==',
                    'node': {
                        'id': 'RGV2RW52OmRldl9lbnYmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJmp1cHl0ZXItdWJ1bnR1JjAuMA==',
                        'info': {
                            'humanName': 'Python 3 Jupyter Notebook for Ubuntu',
                            'name': 'jupyter-ubuntu',
                            'versionMajor': 0,
                            'versionMinor': 0
                        }
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

snapshots['TestEnvironmentDevEnvQueries.test_get_available_dev_env_versions_pagination_reverse 1'] = {
    'data': {
        'availableDevEnvVersions': {
            'edges': [
                {
                    'cursor': 'MQ==',
                    'node': {
                        'id': 'RGV2RW52OmRldl9lbnYmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJmp1cHl0ZXItdWJ1bnR1JjAuMA==',
                        'info': {
                            'humanName': 'Python 3 Jupyter Notebook for Ubuntu',
                            'name': 'jupyter-ubuntu',
                            'versionMajor': 0,
                            'versionMinor': 0
                        }
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

snapshots['TestEnvironmentDevEnvQueries.test_get_available_dev_env_versions_pagination_reverse 2'] = {
    'data': {
        'availableDevEnvVersions': {
            'edges': [
                {
                    'cursor': 'MA==',
                    'node': {
                        'id': 'RGV2RW52OmRldl9lbnYmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJmp1cHl0ZXItdWJ1bnR1JjAuMQ==',
                        'info': {
                            'humanName': 'Python 3 Jupyter Notebook for Ubuntu',
                            'name': 'jupyter-ubuntu',
                            'versionMajor': 0,
                            'versionMinor': 1
                        }
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
