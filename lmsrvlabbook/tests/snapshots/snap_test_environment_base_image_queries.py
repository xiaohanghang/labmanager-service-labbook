# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestEnvironmentBaseImageQueries.test_get_available_base_images 1'] = {
    'data': {
        'availableBaseImages': {
            'edges': [
                {
                    'node': {
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
                },
                {
                    'node': {
                        'author': {
                            'organization': 'Aperture Science'
                        },
                        'availablePackageManagers': [
                            'pip3',
                            'apt-get'
                        ],
                        'component': {
                            'componentClass': 'base_image',
                            'name': 'ubuntu1604-python3-dup',
                            'namespace': 'gigantum',
                            'repository': 'gig-dev_environment-components',
                            'version': '0.2'
                        },
                        'id': 'QmFzZUltYWdlOmJhc2VfaW1hZ2UmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dTE2MDQtcHl0aG9uMy1kdXAmMC4y',
                        'info': {
                            'humanName': 'Ubuntu 16.04 Python 3 Developer Dup',
                            'name': 'ubuntu1604-python3-dup',
                            'versionMajor': 0,
                            'versionMinor': 2
                        },
                        'server': 'hub.docker.com',
                        'tag': '7a7c9d41-2017-08-03'
                    }
                }
            ]
        }
    }
}

snapshots['TestEnvironmentBaseImageQueries.test_get_available_base_images_pagination 1'] = {
    'data': {
        'availableBaseImages': {
            'edges': [
                {
                    'cursor': 'MA==',
                    'node': {
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
                        'namespace': 'gigdev',
                        'repository': 'ubuntu1604-python3',
                        'server': 'hub.docker.com',
                        'tag': '7a7c9d41-2017-08-03'
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
        'availableBaseImages': {
            'edges': [
                {
                    'cursor': 'MQ==',
                    'node': {
                        'info': {
                            'humanName': 'Ubuntu 16.04 Python 3 Developer Dup',
                            'id': 'RW52aXJvbm1lbnRJbmZvOmJhc2VfaW1hZ2UmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dTE2MDQtcHl0aG9uMy1kdXAmMC4y',
                            'name': 'ubuntu1604-python3-dup',
                            'versionMajor': 0,
                            'versionMinor': 2
                        },
                        'namespace': 'gigdev',
                        'repository': 'ubuntu1604-python3',
                        'server': 'hub.docker.com',
                        'tag': '7a7c9d41-2017-08-03'
                    }
                }
            ],
            'pageInfo': {
                'hasNextPage': False
            }
        }
    }
}

snapshots['TestEnvironmentBaseImageQueries.test_get_available_base_images_pagination_reverse 1'] = {
    'data': {
        'availableBaseImages': {
            'edges': [
                {
                    'cursor': 'MQ==',
                    'node': {
                        'id': 'QmFzZUltYWdlOmJhc2VfaW1hZ2UmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dTE2MDQtcHl0aG9uMy1kdXAmMC4y',
                        'info': {
                            'humanName': 'Ubuntu 16.04 Python 3 Developer Dup',
                            'name': 'ubuntu1604-python3-dup',
                            'versionMajor': 0,
                            'versionMinor': 2
                        },
                        'namespace': 'gigdev',
                        'repository': 'ubuntu1604-python3',
                        'server': 'hub.docker.com',
                        'tag': '7a7c9d41-2017-08-03'
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
        'availableBaseImages': {
            'edges': [
                {
                    'cursor': 'MA==',
                    'node': {
                        'info': {
                            'humanName': 'Ubuntu 16.04 Python 3 Developer',
                            'id': 'RW52aXJvbm1lbnRJbmZvOmJhc2VfaW1hZ2UmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dTE2MDQtcHl0aG9uMyYwLjQ=',
                            'name': 'ubuntu1604-python3',
                            'versionMajor': 0,
                            'versionMinor': 4
                        },
                        'namespace': 'gigdev',
                        'repository': 'ubuntu1604-python3',
                        'server': 'hub.docker.com',
                        'tag': '7a7c9d41-2017-08-03'
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
            'component': {
                'componentClass': 'base_image',
                'name': 'ubuntu1604-python3',
                'namespace': 'gigantum',
                'repository': 'gig-dev_environment-components',
                'version': '0.4'
            },
            'info': {
                'humanName': 'Ubuntu 16.04 Python 3 Developer',
                'name': 'ubuntu1604-python3',
                'versionMajor': 0,
                'versionMinor': 4
            }
        }
    }
}

snapshots['TestEnvironmentBaseImageQueries.test_get_available_base_image_versions 1'] = {
    'data': {
        'availableBaseImageVersions': {
            'edges': [
                {
                    'node': {
                        'id': 'QmFzZUltYWdlOmJhc2VfaW1hZ2UmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dTE2MDQtcHl0aG9uMyYwLjQ=',
                        'info': {
                            'humanName': 'Ubuntu 16.04 Python 3 Developer',
                            'name': 'ubuntu1604-python3',
                            'versionMajor': 0,
                            'versionMinor': 4
                        }
                    }
                },
                {
                    'node': {
                        'id': 'QmFzZUltYWdlOmJhc2VfaW1hZ2UmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dTE2MDQtcHl0aG9uMyYwLjM=',
                        'info': {
                            'humanName': 'Ubuntu 16.04 Python 3 Developer',
                            'name': 'ubuntu1604-python3',
                            'versionMajor': 0,
                            'versionMinor': 3
                        }
                    }
                },
                {
                    'node': {
                        'id': 'QmFzZUltYWdlOmJhc2VfaW1hZ2UmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dTE2MDQtcHl0aG9uMyYwLjI=',
                        'info': {
                            'humanName': 'Ubuntu 16.04 Python 3 Developer',
                            'name': 'ubuntu1604-python3',
                            'versionMajor': 0,
                            'versionMinor': 2
                        }
                    }
                }
            ]
        }
    }
}

snapshots['TestEnvironmentBaseImageQueries.test_get_available_base_image_versions_pagination 1'] = {
    'data': {
        'availableBaseImageVersions': {
            'edges': [
                {
                    'cursor': 'MA==',
                    'node': {
                        'id': 'QmFzZUltYWdlOmJhc2VfaW1hZ2UmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dTE2MDQtcHl0aG9uMyYwLjQ=',
                        'info': {
                            'humanName': 'Ubuntu 16.04 Python 3 Developer',
                            'name': 'ubuntu1604-python3',
                            'versionMajor': 0,
                            'versionMinor': 4
                        }
                    }
                },
                {
                    'cursor': 'MQ==',
                    'node': {
                        'id': 'QmFzZUltYWdlOmJhc2VfaW1hZ2UmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dTE2MDQtcHl0aG9uMyYwLjM=',
                        'info': {
                            'humanName': 'Ubuntu 16.04 Python 3 Developer',
                            'name': 'ubuntu1604-python3',
                            'versionMajor': 0,
                            'versionMinor': 3
                        }
                    }
                },
                {
                    'cursor': 'Mg==',
                    'node': {
                        'id': 'QmFzZUltYWdlOmJhc2VfaW1hZ2UmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dTE2MDQtcHl0aG9uMyYwLjI=',
                        'info': {
                            'humanName': 'Ubuntu 16.04 Python 3 Developer',
                            'name': 'ubuntu1604-python3',
                            'versionMajor': 0,
                            'versionMinor': 2
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

snapshots['TestEnvironmentBaseImageQueries.test_get_available_base_image_versions_pagination 2'] = {
    'data': {
        'availableBaseImageVersions': {
            'edges': [
                {
                    'cursor': 'Mw==',
                    'node': {
                        'id': 'QmFzZUltYWdlOmJhc2VfaW1hZ2UmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dTE2MDQtcHl0aG9uMyYwLjE=',
                        'info': {
                            'humanName': 'Ubuntu 16.04 Python 3 Developer',
                            'name': 'ubuntu1604-python3',
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

snapshots['TestEnvironmentBaseImageQueries.test_get_available_base_image_versions_pagination_reverse 1'] = {
    'data': {
        'availableBaseImageVersions': {
            'edges': [
                {
                    'cursor': 'MQ==',
                    'node': {
                        'id': 'QmFzZUltYWdlOmJhc2VfaW1hZ2UmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dTE2MDQtcHl0aG9uMyYwLjM=',
                        'info': {
                            'humanName': 'Ubuntu 16.04 Python 3 Developer',
                            'name': 'ubuntu1604-python3',
                            'versionMajor': 0,
                            'versionMinor': 3
                        }
                    }
                },
                {
                    'cursor': 'Mg==',
                    'node': {
                        'id': 'QmFzZUltYWdlOmJhc2VfaW1hZ2UmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dTE2MDQtcHl0aG9uMyYwLjI=',
                        'info': {
                            'humanName': 'Ubuntu 16.04 Python 3 Developer',
                            'name': 'ubuntu1604-python3',
                            'versionMajor': 0,
                            'versionMinor': 2
                        }
                    }
                },
                {
                    'cursor': 'Mw==',
                    'node': {
                        'id': 'QmFzZUltYWdlOmJhc2VfaW1hZ2UmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dTE2MDQtcHl0aG9uMyYwLjE=',
                        'info': {
                            'humanName': 'Ubuntu 16.04 Python 3 Developer',
                            'name': 'ubuntu1604-python3',
                            'versionMajor': 0,
                            'versionMinor': 1
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

snapshots['TestEnvironmentBaseImageQueries.test_get_available_base_image_versions_pagination_reverse 2'] = {
    'data': {
        'availableBaseImageVersions': {
            'edges': [
                {
                    'cursor': 'MA==',
                    'node': {
                        'id': 'QmFzZUltYWdlOmJhc2VfaW1hZ2UmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dTE2MDQtcHl0aG9uMyYwLjQ=',
                        'info': {
                            'humanName': 'Ubuntu 16.04 Python 3 Developer',
                            'name': 'ubuntu1604-python3',
                            'versionMajor': 0,
                            'versionMinor': 4
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
