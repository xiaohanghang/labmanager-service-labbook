# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestEnvironmentCustomDependencyQueries.test_get_available_custom_deps 1'] = {
    'data': {
        'availableCustomDependencies': {
            'edges': [
                {
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
                },
                {
                    'node': {
                        'author': {
                            'organization': 'Aperture Science'
                        },
                        'component': {
                            'componentClass': 'custom',
                            'name': 'ubuntu-python3-pillow-dup',
                            'namespace': 'gigantum',
                            'repository': 'gig-dev_environment-components',
                            'version': '0.2'
                        },
                        'docker': '''RUN apt-get -y install libjpeg-dev libtiff5-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjpeg-dev
RUN pip3 install Pillow==4.2.1 
''',
                        'id': 'Q3VzdG9tRGVwZW5kZW5jeTpjdXN0b20mZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dS1weXRob24zLXBpbGxvdy1kdXAmMC4y',
                        'info': {
                            'humanName': 'Pillow',
                            'name': 'ubuntu-python3-pillow-dup',
                            'versionMajor': 0,
                            'versionMinor': 2
                        },
                        'osBaseClass': 'ubuntu'
                    }
                }
            ]
        }
    }
}

snapshots['TestEnvironmentCustomDependencyQueries.test_get_available_custom_deps_pagination 1'] = {
    'data': {
        'availableCustomDependencies': {
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
                'hasNextPage': True,
                'hasPreviousPage': False
            }
        }
    }
}

snapshots['TestEnvironmentCustomDependencyQueries.test_get_available_custom_deps_pagination 2'] = {
    'data': {
        'availableCustomDependencies': {
            'edges': [
                {
                    'cursor': 'MQ==',
                    'node': {
                        'author': {
                            'organization': 'Aperture Science'
                        },
                        'component': {
                            'componentClass': 'custom',
                            'name': 'ubuntu-python3-pillow-dup',
                            'namespace': 'gigantum',
                            'repository': 'gig-dev_environment-components',
                            'version': '0.2'
                        },
                        'docker': '''RUN apt-get -y install libjpeg-dev libtiff5-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjpeg-dev
RUN pip3 install Pillow==4.2.1 
''',
                        'id': 'Q3VzdG9tRGVwZW5kZW5jeTpjdXN0b20mZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dS1weXRob24zLXBpbGxvdy1kdXAmMC4y',
                        'info': {
                            'humanName': 'Pillow',
                            'name': 'ubuntu-python3-pillow-dup',
                            'versionMajor': 0,
                            'versionMinor': 2
                        },
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

snapshots['TestEnvironmentCustomDependencyQueries.test_get_available_custom_deps_pagination_reverse 1'] = {
    'data': {
        'availableCustomDependencies': {
            'edges': [
                {
                    'cursor': 'MQ==',
                    'node': {
                        'author': {
                            'organization': 'Aperture Science'
                        },
                        'component': {
                            'componentClass': 'custom',
                            'name': 'ubuntu-python3-pillow-dup',
                            'namespace': 'gigantum',
                            'repository': 'gig-dev_environment-components',
                            'version': '0.2'
                        },
                        'docker': '''RUN apt-get -y install libjpeg-dev libtiff5-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjpeg-dev
RUN pip3 install Pillow==4.2.1 
''',
                        'id': 'Q3VzdG9tRGVwZW5kZW5jeTpjdXN0b20mZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dS1weXRob24zLXBpbGxvdy1kdXAmMC4y',
                        'info': {
                            'humanName': 'Pillow',
                            'name': 'ubuntu-python3-pillow-dup',
                            'versionMajor': 0,
                            'versionMinor': 2
                        },
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

snapshots['TestEnvironmentCustomDependencyQueries.test_get_available_custom_deps_pagination_reverse 2'] = {
    'data': {
        'availableCustomDependencies': {
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
                'hasNextPage': False,
                'hasPreviousPage': False
            }
        }
    }
}

snapshots['TestEnvironmentCustomDependencyQueries.test_get_custom_deps_by_node 1'] = {
    'data': {
        'node': {
            'component': {
                'componentClass': 'custom',
                'name': 'ubuntu-python3-pillow',
                'namespace': 'gigantum',
                'repository': 'gig-dev_environment-components',
                'version': '0.1'
            },
            'info': {
                'humanName': 'Pillow',
                'name': 'ubuntu-python3-pillow',
                'versionMajor': 0,
                'versionMinor': 1
            }
        }
    }
}

snapshots['TestEnvironmentCustomDependencyQueries.test_get_available_custom_deps_versions 1'] = {
    'data': {
        'availableCustomDependenciesVersions': {
            'edges': [
                {
                    'cursor': 'MA==',
                    'node': {
                        'component': {
                            'componentClass': 'custom',
                            'name': 'ubuntu-python3-pillow',
                            'namespace': 'gigantum',
                            'repository': 'gig-dev_environment-components',
                            'version': '0.3'
                        },
                        'id': 'Q3VzdG9tRGVwZW5kZW5jeTpjdXN0b20mZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dS1weXRob24zLXBpbGxvdyYwLjM=',
                        'info': {
                            'humanName': 'Pillow',
                            'name': 'ubuntu-python3-pillow',
                            'versionMajor': 0,
                            'versionMinor': 3
                        }
                    }
                },
                {
                    'cursor': 'MQ==',
                    'node': {
                        'component': {
                            'componentClass': 'custom',
                            'name': 'ubuntu-python3-pillow',
                            'namespace': 'gigantum',
                            'repository': 'gig-dev_environment-components',
                            'version': '0.2'
                        },
                        'id': 'Q3VzdG9tRGVwZW5kZW5jeTpjdXN0b20mZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dS1weXRob24zLXBpbGxvdyYwLjI=',
                        'info': {
                            'humanName': 'Pillow',
                            'name': 'ubuntu-python3-pillow',
                            'versionMajor': 0,
                            'versionMinor': 2
                        }
                    }
                },
                {
                    'cursor': 'Mg==',
                    'node': {
                        'component': {
                            'componentClass': 'custom',
                            'name': 'ubuntu-python3-pillow',
                            'namespace': 'gigantum',
                            'repository': 'gig-dev_environment-components',
                            'version': '0.1'
                        },
                        'id': 'Q3VzdG9tRGVwZW5kZW5jeTpjdXN0b20mZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dS1weXRob24zLXBpbGxvdyYwLjE=',
                        'info': {
                            'humanName': 'Pillow',
                            'name': 'ubuntu-python3-pillow',
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

snapshots['TestEnvironmentCustomDependencyQueries.test_get_available_custom_deps_versions_pagination 1'] = {
    'data': {
        'availableCustomDependenciesVersions': {
            'edges': [
                {
                    'cursor': 'MA==',
                    'node': {
                        'component': {
                            'componentClass': 'custom',
                            'name': 'ubuntu-python3-pillow',
                            'namespace': 'gigantum',
                            'repository': 'gig-dev_environment-components',
                            'version': '0.3'
                        },
                        'id': 'Q3VzdG9tRGVwZW5kZW5jeTpjdXN0b20mZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dS1weXRob24zLXBpbGxvdyYwLjM=',
                        'info': {
                            'humanName': 'Pillow',
                            'name': 'ubuntu-python3-pillow',
                            'versionMajor': 0,
                            'versionMinor': 3
                        }
                    }
                },
                {
                    'cursor': 'MQ==',
                    'node': {
                        'component': {
                            'componentClass': 'custom',
                            'name': 'ubuntu-python3-pillow',
                            'namespace': 'gigantum',
                            'repository': 'gig-dev_environment-components',
                            'version': '0.2'
                        },
                        'id': 'Q3VzdG9tRGVwZW5kZW5jeTpjdXN0b20mZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dS1weXRob24zLXBpbGxvdyYwLjI=',
                        'info': {
                            'humanName': 'Pillow',
                            'name': 'ubuntu-python3-pillow',
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

snapshots['TestEnvironmentCustomDependencyQueries.test_get_available_custom_deps_versions_pagination 2'] = {
    'data': {
        'availableCustomDependenciesVersions': {
            'edges': [
                {
                    'cursor': 'Mg==',
                    'node': {
                        'component': {
                            'componentClass': 'custom',
                            'name': 'ubuntu-python3-pillow',
                            'namespace': 'gigantum',
                            'repository': 'gig-dev_environment-components',
                            'version': '0.1'
                        },
                        'id': 'Q3VzdG9tRGVwZW5kZW5jeTpjdXN0b20mZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dS1weXRob24zLXBpbGxvdyYwLjE=',
                        'info': {
                            'humanName': 'Pillow',
                            'name': 'ubuntu-python3-pillow',
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

snapshots['TestEnvironmentCustomDependencyQueries.test_get_available_custom_deps_versions_pagination_reverse 1'] = {
    'data': {
        'availableCustomDependenciesVersions': {
            'edges': [
                {
                    'cursor': 'MQ==',
                    'node': {
                        'component': {
                            'componentClass': 'custom',
                            'name': 'ubuntu-python3-pillow',
                            'namespace': 'gigantum',
                            'repository': 'gig-dev_environment-components',
                            'version': '0.2'
                        },
                        'id': 'Q3VzdG9tRGVwZW5kZW5jeTpjdXN0b20mZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dS1weXRob24zLXBpbGxvdyYwLjI=',
                        'info': {
                            'humanName': 'Pillow',
                            'name': 'ubuntu-python3-pillow',
                            'versionMajor': 0,
                            'versionMinor': 2
                        }
                    }
                },
                {
                    'cursor': 'Mg==',
                    'node': {
                        'component': {
                            'componentClass': 'custom',
                            'name': 'ubuntu-python3-pillow',
                            'namespace': 'gigantum',
                            'repository': 'gig-dev_environment-components',
                            'version': '0.1'
                        },
                        'id': 'Q3VzdG9tRGVwZW5kZW5jeTpjdXN0b20mZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dS1weXRob24zLXBpbGxvdyYwLjE=',
                        'info': {
                            'humanName': 'Pillow',
                            'name': 'ubuntu-python3-pillow',
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

snapshots['TestEnvironmentCustomDependencyQueries.test_get_available_custom_deps_versions_pagination_reverse 2'] = {
    'data': {
        'availableCustomDependenciesVersions': {
            'edges': [
                {
                    'cursor': 'MA==',
                    'node': {
                        'component': {
                            'componentClass': 'custom',
                            'name': 'ubuntu-python3-pillow',
                            'namespace': 'gigantum',
                            'repository': 'gig-dev_environment-components',
                            'version': '0.3'
                        },
                        'id': 'Q3VzdG9tRGVwZW5kZW5jeTpjdXN0b20mZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dS1weXRob24zLXBpbGxvdyYwLjM=',
                        'info': {
                            'humanName': 'Pillow',
                            'name': 'ubuntu-python3-pillow',
                            'versionMajor': 0,
                            'versionMinor': 3
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
