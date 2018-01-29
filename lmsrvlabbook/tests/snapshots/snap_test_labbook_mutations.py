# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestLabBookServiceMutations.test_makedir 1'] = {
    'data': {
        'makeLabbookDirectory': {
            'newLabbookFileEdge': {
                'node': {
                    'isDir': True,
                    'key': 'new_folder/',
                    'size': 0
                }
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_move_file_many 1'] = {
    'data': {
        'moveLabbookFile': {
            'newLabbookFileEdge': {
                'node': {
                    'isDir': False,
                    'key': 'subdir/sillyfile',
                    'size': 7
                }
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_move_file_many 2'] = {
    'data': {
        'moveLabbookFile': {
            'newLabbookFileEdge': {
                'node': {
                    'isDir': False,
                    'key': 'sillyfile',
                    'size': 7
                }
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_move_file_many 3'] = {
    'data': {
        'moveLabbookFile': {
            'newLabbookFileEdge': {
                'node': {
                    'isDir': False,
                    'key': 'subdir/sillyfile',
                    'size': 7
                }
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_move_file_many 4'] = {
    'data': {
        'moveLabbookFile': {
            'newLabbookFileEdge': {
                'node': {
                    'isDir': False,
                    'key': 'sillyfile',
                    'size': 7
                }
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_move_file_many 5'] = {
    'data': {
        'moveLabbookFile': {
            'newLabbookFileEdge': {
                'node': {
                    'isDir': False,
                    'key': 'subdir/sillyfile',
                    'size': 7
                }
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_move_file_many 6'] = {
    'data': {
        'moveLabbookFile': {
            'newLabbookFileEdge': {
                'node': {
                    'isDir': False,
                    'key': 'sillyfile',
                    'size': 7
                }
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_add_file 1'] = {
    'data': {
        'addLabbookFile': {
            'newLabbookFileEdge': None
        }
    }
}

snapshots['TestLabBookServiceMutations.test_add_file 2'] = {
    'data': {
        'addLabbookFile': {
            'newLabbookFileEdge': None
        }
    }
}

snapshots['TestLabBookServiceMutations.test_add_file 3'] = {
    'data': {
        'addLabbookFile': {
            'newLabbookFileEdge': {
                'node': {
                    'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJm15ZmlsZS5iaW4=',
                    'isDir': False,
                    'key': 'myfile.bin',
                    'size': 9000000
                }
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_add_file_errors 1'] = {
    'data': {
        'addLabbookFile': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 23,
                    'line': 3
                }
            ],
            'message': 'No file "uploadChunk" associated with request'
        }
    ]
}

snapshots['TestLabBookServiceMutations.test_rename_labbook 1'] = {
    'data': {
        'renameLabbook': {
            'success': True
        }
    }
}

snapshots['TestLabBookServiceMutations.test_add_favorite 1'] = {
    'data': {
        'labbook': {
            'code': {
                'favorites': {
                    'edges': [
                    ]
                }
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceMutations.test_add_favorite 2'] = {
    'data': {
        'addFavorite': {
            'newFavoriteEdge': {
                'node': {
                    'description': 'my test favorite',
                    'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSYw',
                    'index': 0,
                    'isDir': False,
                    'key': 'test.txt'
                }
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_add_favorite 3'] = {
    'data': {
        'labbook': {
            'code': {
                'favorites': {
                    'edges': [
                        {
                            'node': {
                                'description': 'my test favorite',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSYw',
                                'index': 0,
                                'isDir': False,
                                'key': 'test.txt'
                            }
                        }
                    ]
                }
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceMutations.test_add_favorite_dir 1'] = {
    'data': {
        'labbook': {
            'input': {
                'favorites': {
                    'edges': [
                    ]
                }
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceMutations.test_add_favorite_dir 2'] = {
    'data': {
        'addFavorite': {
            'newFavoriteEdge': {
                'node': {
                    'description': 'my data dir',
                    'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmaW5wdXQmMA==',
                    'index': 0,
                    'isDir': True,
                    'key': 'sample1/'
                }
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_add_favorite_dir 3'] = {
    'data': {
        'labbook': {
            'input': {
                'favorites': {
                    'edges': [
                        {
                            'node': {
                                'description': 'my data dir',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmaW5wdXQmMA==',
                                'index': 0,
                                'isDir': True,
                                'key': 'sample1/'
                            }
                        }
                    ]
                }
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceMutations.test_add_favorite_dir 4'] = {
    'data': {
        'addFavorite': {
            'newFavoriteEdge': {
                'node': {
                    'description': 'my data dir 2',
                    'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmaW5wdXQmMQ==',
                    'index': 1,
                    'isDir': True,
                    'key': 'sample2/'
                }
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_add_favorite_dir 5'] = {
    'data': {
        'labbook': {
            'input': {
                'favorites': {
                    'edges': [
                        {
                            'node': {
                                'description': 'my data dir',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmaW5wdXQmMA==',
                                'index': 0,
                                'isDir': True,
                                'key': 'sample1/'
                            }
                        },
                        {
                            'node': {
                                'description': 'my data dir 2',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmaW5wdXQmMQ==',
                                'index': 1,
                                'isDir': True,
                                'key': 'sample2/'
                            }
                        }
                    ]
                }
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceMutations.test_add_favorite_at_index 1'] = {
    'data': {
        'labbook': {
            'code': {
                'favorites': {
                    'edges': [
                    ]
                }
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceMutations.test_add_favorite_at_index 2'] = {
    'data': {
        'addFavorite': {
            'newFavoriteEdge': {
                'node': {
                    'description': 'my test favorite 1',
                    'index': 0,
                    'key': 'test1.txt'
                }
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_add_favorite_at_index 3'] = {
    'data': {
        'addFavorite': {
            'newFavoriteEdge': {
                'node': {
                    'description': 'my test favorite 2',
                    'index': 1,
                    'key': 'test2.txt'
                }
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_add_favorite_at_index 4'] = {
    'data': {
        'addFavorite': {
            'newFavoriteEdge': {
                'node': {
                    'description': 'my test favorite 3',
                    'index': 1,
                    'key': 'test3.txt'
                }
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_add_favorite_at_index 5'] = {
    'data': {
        'labbook': {
            'code': {
                'favorites': {
                    'edges': [
                        {
                            'node': {
                                'description': 'my test favorite 1',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSYw',
                                'index': 0,
                                'isDir': False,
                                'key': 'test1.txt'
                            }
                        },
                        {
                            'node': {
                                'description': 'my test favorite 3',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSYx',
                                'index': 1,
                                'isDir': False,
                                'key': 'test3.txt'
                            }
                        },
                        {
                            'node': {
                                'description': 'my test favorite 2',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSYy',
                                'index': 2,
                                'isDir': False,
                                'key': 'test2.txt'
                            }
                        }
                    ]
                }
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceMutations.test_delete_favorite 1'] = {
    'data': {
        'addFavorite': {
            'newFavoriteEdge': {
                'node': {
                    'description': 'my test favorite',
                    'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSYw',
                    'index': 0,
                    'isDir': False,
                    'key': 'test.txt'
                }
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_delete_favorite 2'] = {
    'data': {
        'labbook': {
            'code': {
                'favorites': {
                    'edges': [
                        {
                            'node': {
                                'description': 'my test favorite',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSYw',
                                'index': 0,
                                'isDir': False,
                                'key': 'test.txt'
                            }
                        }
                    ]
                }
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceMutations.test_delete_favorite 3'] = {
    'data': {
        'removeFavorite': {
            'success': True
        }
    }
}

snapshots['TestLabBookServiceMutations.test_delete_favorite 4'] = {
    'data': {
        'labbook': {
            'code': {
                'favorites': {
                    'edges': [
                    ]
                }
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceMutations.test_update_favorite 1'] = {
    'data': {
        'labbook': {
            'code': {
                'favorites': {
                    'edges': [
                    ]
                }
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceMutations.test_update_favorite 2'] = {
    'data': {
        'addFavorite': {
            'newFavoriteEdge': {
                'node': {
                    'description': 'my test favorite',
                    'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSYw',
                    'index': 0,
                    'isDir': False,
                    'key': 'test.txt'
                }
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_update_favorite 3'] = {
    'data': {
        'labbook': {
            'code': {
                'favorites': {
                    'edges': [
                        {
                            'node': {
                                'description': 'my test favorite',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSYw',
                                'index': 0,
                                'isDir': False,
                                'key': 'test.txt'
                            }
                        }
                    ]
                }
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceMutations.test_move_file 1'] = {
    'data': {
        'moveLabbookFile': {
            'newLabbookFileEdge': {
                'node': {
                    'isDir': False,
                    'key': 'subdir/sillyfile',
                    'size': 7
                }
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_move_file 2'] = {
    'data': {
        'moveLabbookFile': {
            'newLabbookFileEdge': {
                'node': {
                    'isDir': True,
                    'key': 'subdir2/',
                    'size': 0
                }
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_update_favorite 4'] = {
    'data': {
        'updateFavorite': {
            'updatedFavoriteEdge': {
                'node': {
                    'description': 'UPDATED',
                    'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSYw',
                    'index': 0,
                    'isDir': False,
                    'key': 'test2.txt'
                }
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_update_favorite 5'] = {
    'data': {
        'labbook': {
            'code': {
                'favorites': {
                    'edges': [
                        {
                            'node': {
                                'description': 'UPDATED',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSYw',
                                'index': 0,
                                'isDir': False,
                                'key': 'test2.txt'
                            }
                        }
                    ]
                }
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceMutations.test_create_labbook 1'] = {
    'data': {
        'createLabbook': {
            'labbook': {
                'description': 'my test description',
                'id': 'TGFiYm9vazpkZWZhdWx0JnRlc3QtbGFiLWJvb2sx',
                'name': 'test-lab-book1'
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_create_labbook_already_exists 1'] = {
    'data': {
        'createLabbook': {
            'labbook': {
                'description': 'my test description',
                'id': 'TGFiYm9vazpkZWZhdWx0JnRlc3QtbGFiLWR1cGxpY2F0ZQ==',
                'name': 'test-lab-duplicate'
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_create_labbook_already_exists 2'] = {
    'data': {
        'labbook': {
            'description': 'my test description',
            'name': 'test-lab-duplicate'
        }
    }
}

snapshots['TestLabBookServiceMutations.test_create_labbook_already_exists 3'] = {
    'data': {
        'createLabbook': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 11,
                    'line': 4
                }
            ],
            'message': 'LabBook `test-lab-duplicate` already exists locally. Choose a new LabBook name'
        }
    ]
}

snapshots['TestLabBookServiceMutations.test_create_labbook 2'] = {
    'data': {
        'labbook': {
            'activityRecords': {
                'edges': [
                    {
                        'node': {
                            'detailObjects': [
                                {
                                    'data': [
                                        [
                                            'text/plain',
                                            '''Added a `base` class environment component quickstart-jupyterlab

Data Science Quickstart using Jupyterlab, numpy, and Matplotlib. A great base for any analysis.

  - repository: gig-dev_components2
  - component: quickstart-jupyterlab
  - revision: 1
'''
                                        ]
                                    ],
                                    'importance': 0,
                                    'show': False,
                                    'tags': [
                                    ],
                                    'type': 'ENVIRONMENT'
                                }
                            ],
                            'importance': 0,
                            'message': 'Add base environment component: quickstart-jupyterlab',
                            'show': True,
                            'tags': [
                                'environment',
                                'base'
                            ],
                            'type': 'ENVIRONMENT'
                        }
                    },
                    {
                        'node': {
                            'detailObjects': [
                                {
                                    'data': [
                                        [
                                            'text/plain',
                                            'Add pip3 managed package: pandas v0.22.0'
                                        ]
                                    ],
                                    'importance': 0,
                                    'show': False,
                                    'tags': [
                                    ],
                                    'type': 'ENVIRONMENT'
                                }
                            ],
                            'importance': 0,
                            'message': 'Add pip3 managed package: pandas v0.22.0',
                            'show': True,
                            'tags': [
                                'environment',
                                'package_manager',
                                'pip3'
                            ],
                            'type': 'ENVIRONMENT'
                        }
                    },
                    {
                        'node': {
                            'detailObjects': [
                                {
                                    'data': [
                                        [
                                            'text/plain',
                                            'Add pip3 managed package: ipywidgets v7.1.0'
                                        ]
                                    ],
                                    'importance': 0,
                                    'show': False,
                                    'tags': [
                                    ],
                                    'type': 'ENVIRONMENT'
                                }
                            ],
                            'importance': 0,
                            'message': 'Add pip3 managed package: ipywidgets v7.1.0',
                            'show': True,
                            'tags': [
                                'environment',
                                'package_manager',
                                'pip3'
                            ],
                            'type': 'ENVIRONMENT'
                        }
                    },
                    {
                        'node': {
                            'detailObjects': [
                                {
                                    'data': [
                                        [
                                            'text/plain',
                                            'Add pip3 managed package: jupyterlab v0.31.1'
                                        ]
                                    ],
                                    'importance': 0,
                                    'show': False,
                                    'tags': [
                                    ],
                                    'type': 'ENVIRONMENT'
                                }
                            ],
                            'importance': 0,
                            'message': 'Add pip3 managed package: jupyterlab v0.31.1',
                            'show': True,
                            'tags': [
                                'environment',
                                'package_manager',
                                'pip3'
                            ],
                            'type': 'ENVIRONMENT'
                        }
                    },
                    {
                        'node': {
                            'detailObjects': [
                                {
                                    'data': [
                                        [
                                            'text/plain',
                                            'Add pip3 managed package: jupyter v1.0.0'
                                        ]
                                    ],
                                    'importance': 0,
                                    'show': False,
                                    'tags': [
                                    ],
                                    'type': 'ENVIRONMENT'
                                }
                            ],
                            'importance': 0,
                            'message': 'Add pip3 managed package: jupyter v1.0.0',
                            'show': True,
                            'tags': [
                                'environment',
                                'package_manager',
                                'pip3'
                            ],
                            'type': 'ENVIRONMENT'
                        }
                    },
                    {
                        'node': {
                            'detailObjects': [
                                {
                                    'data': [
                                        [
                                            'text/plain',
                                            'Add pip3 managed package: matplotlib v2.1.1'
                                        ]
                                    ],
                                    'importance': 0,
                                    'show': False,
                                    'tags': [
                                    ],
                                    'type': 'ENVIRONMENT'
                                }
                            ],
                            'importance': 0,
                            'message': 'Add pip3 managed package: matplotlib v2.1.1',
                            'show': True,
                            'tags': [
                                'environment',
                                'package_manager',
                                'pip3'
                            ],
                            'type': 'ENVIRONMENT'
                        }
                    },
                    {
                        'node': {
                            'detailObjects': [
                                {
                                    'data': [
                                        [
                                            'text/plain',
                                            'Add pip3 managed package: numpy v1.14.0'
                                        ]
                                    ],
                                    'importance': 0,
                                    'show': False,
                                    'tags': [
                                    ],
                                    'type': 'ENVIRONMENT'
                                }
                            ],
                            'importance': 0,
                            'message': 'Add pip3 managed package: numpy v1.14.0',
                            'show': True,
                            'tags': [
                                'environment',
                                'package_manager',
                                'pip3'
                            ],
                            'type': 'ENVIRONMENT'
                        }
                    },
                    {
                        'node': {
                            'detailObjects': [
                                {
                                    'data': [
                                        [
                                            'text/plain',
                                            'Add apt managed package: vim vNone'
                                        ]
                                    ],
                                    'importance': 0,
                                    'show': False,
                                    'tags': [
                                    ],
                                    'type': 'ENVIRONMENT'
                                }
                            ],
                            'importance': 0,
                            'message': 'Add apt managed package: vim vNone',
                            'show': True,
                            'tags': [
                                'environment',
                                'package_manager',
                                'apt'
                            ],
                            'type': 'ENVIRONMENT'
                        }
                    },
                    {
                        'node': {
                            'detailObjects': [
                                {
                                    'data': [
                                        [
                                            'text/plain',
                                            'Update apt managed package: curl vNone'
                                        ]
                                    ],
                                    'importance': 0,
                                    'show': False,
                                    'tags': [
                                    ],
                                    'type': 'ENVIRONMENT'
                                }
                            ],
                            'importance': 0,
                            'message': 'Update apt managed package: curl vNone',
                            'show': True,
                            'tags': [
                                'environment',
                                'package_manager',
                                'apt'
                            ],
                            'type': 'ENVIRONMENT'
                        }
                    },
                    {
                        'node': {
                            'detailObjects': [
                                {
                                    'data': [
                                        [
                                            'text/plain',
                                            'Add apt managed package: git vNone'
                                        ]
                                    ],
                                    'importance': 0,
                                    'show': False,
                                    'tags': [
                                    ],
                                    'type': 'ENVIRONMENT'
                                }
                            ],
                            'importance': 0,
                            'message': 'Add apt managed package: git vNone',
                            'show': True,
                            'tags': [
                                'environment',
                                'package_manager',
                                'apt'
                            ],
                            'type': 'ENVIRONMENT'
                        }
                    },
                    {
                        'node': {
                            'detailObjects': [
                                {
                                    'data': [
                                        [
                                            'text/plain',
                                            'Add apt managed package: python3-pip vNone'
                                        ]
                                    ],
                                    'importance': 0,
                                    'show': False,
                                    'tags': [
                                    ],
                                    'type': 'ENVIRONMENT'
                                }
                            ],
                            'importance': 0,
                            'message': 'Add apt managed package: python3-pip vNone',
                            'show': True,
                            'tags': [
                                'environment',
                                'package_manager',
                                'apt'
                            ],
                            'type': 'ENVIRONMENT'
                        }
                    },
                    {
                        'node': {
                            'detailObjects': [
                                {
                                    'data': [
                                        [
                                            'text/plain',
                                            'Add apt managed package: python3-dev vNone'
                                        ]
                                    ],
                                    'importance': 0,
                                    'show': False,
                                    'tags': [
                                    ],
                                    'type': 'ENVIRONMENT'
                                }
                            ],
                            'importance': 0,
                            'message': 'Add apt managed package: python3-dev vNone',
                            'show': True,
                            'tags': [
                                'environment',
                                'package_manager',
                                'apt'
                            ],
                            'type': 'ENVIRONMENT'
                        }
                    },
                    {
                        'node': {
                            'detailObjects': [
                                {
                                    'data': [
                                        [
                                            'text/plain',
                                            'Add apt managed package: build-essential vNone'
                                        ]
                                    ],
                                    'importance': 0,
                                    'show': False,
                                    'tags': [
                                    ],
                                    'type': 'ENVIRONMENT'
                                }
                            ],
                            'importance': 0,
                            'message': 'Add apt managed package: build-essential vNone',
                            'show': True,
                            'tags': [
                                'environment',
                                'package_manager',
                                'apt'
                            ],
                            'type': 'ENVIRONMENT'
                        }
                    },
                    {
                        'node': {
                            'detailObjects': [
                                {
                                    'data': [
                                        [
                                            'text/plain',
                                            'Add apt managed package: gosu vNone'
                                        ]
                                    ],
                                    'importance': 0,
                                    'show': False,
                                    'tags': [
                                    ],
                                    'type': 'ENVIRONMENT'
                                }
                            ],
                            'importance': 0,
                            'message': 'Add apt managed package: gosu vNone',
                            'show': True,
                            'tags': [
                                'environment',
                                'package_manager',
                                'apt'
                            ],
                            'type': 'ENVIRONMENT'
                        }
                    },
                    {
                        'node': {
                            'detailObjects': [
                                {
                                    'data': [
                                        [
                                            'text/plain',
                                            'Add apt managed package: curl vNone'
                                        ]
                                    ],
                                    'importance': 0,
                                    'show': False,
                                    'tags': [
                                    ],
                                    'type': 'ENVIRONMENT'
                                }
                            ],
                            'importance': 0,
                            'message': 'Add apt managed package: curl vNone',
                            'show': True,
                            'tags': [
                                'environment',
                                'package_manager',
                                'apt'
                            ],
                            'type': 'ENVIRONMENT'
                        }
                    },
                    {
                        'node': {
                            'detailObjects': [
                                {
                                    'data': [
                                        [
                                            'text/plain',
                                            'Add apt managed package: supervisor vNone'
                                        ]
                                    ],
                                    'importance': 0,
                                    'show': False,
                                    'tags': [
                                    ],
                                    'type': 'ENVIRONMENT'
                                }
                            ],
                            'importance': 0,
                            'message': 'Add apt managed package: supervisor vNone',
                            'show': True,
                            'tags': [
                                'environment',
                                'package_manager',
                                'apt'
                            ],
                            'type': 'ENVIRONMENT'
                        }
                    },
                    {
                        'node': {
                            'detailObjects': [
                                {
                                    'data': [
                                        [
                                            'text/plain',
                                            'Created new LabBook: default/test-lab-book1'
                                        ]
                                    ],
                                    'importance': 0,
                                    'show': False,
                                    'tags': [
                                    ],
                                    'type': 'LABBOOK'
                                }
                            ],
                            'importance': 255,
                            'message': 'Created new LabBook: default/test-lab-book1',
                            'show': True,
                            'tags': None,
                            'type': 'LABBOOK'
                        }
                    }
                ]
            }
        }
    }
}
