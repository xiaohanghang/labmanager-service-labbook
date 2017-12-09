# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestLabBookServiceMutations.test_create_labbook_already_exists 1'] = {
    'data': {
        'createLabbook': {
            'labbook': {
                'description': 'my test description',
                'name': 'test-lab-book'
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_create_labbook_already_exists 2'] = {
    'data': {
        'createLabbook': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 15,
                    'line': 3
                }
            ],
            'message': 'LabBook `test-lab-book` already exists locally. Choose a new LabBook name'
        }
    ]
}

snapshots['TestLabBookServiceMutations.test_create_branch 1'] = {
    'data': {
        'labbook': {
            'activeBranch': {
                'name': 'master'
            },
            'branches': {
                'edges': [
                    {
                        'node': {
                            'name': 'dev-branch-1'
                        }
                    },
                    {
                        'node': {
                            'name': 'master'
                        }
                    }
                ]
            },
            'description': 'Yada yada blah blah blah 99',
            'name': 'test-lab-book2'
        }
    }
}

snapshots['TestLabBookServiceMutations.test_checkout_branch 1'] = {
    'data': {
        'createBranch': {
            'branch': {
                'name': 'dev-branch-5'
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_checkout_branch 2'] = {
    'data': {
        'labbook': {
            'activeBranch': {
                'name': 'master'
            },
            'branches': {
                'edges': [
                    {
                        'node': {
                            'name': 'dev-branch-5',
                            'prefix': None
                        }
                    },
                    {
                        'node': {
                            'name': 'master',
                            'prefix': None
                        }
                    }
                ]
            },
            'description': 'a different description',
            'name': 'test-lab-book3'
        }
    }
}

snapshots['TestLabBookServiceMutations.test_checkout_branch 3'] = {
    'data': {
        'labbook': {
            'activeBranch': {
                'name': 'dev-branch-5',
                'prefix': None
            },
            'description': 'a different description',
            'name': 'test-lab-book3'
        }
    }
}

snapshots['TestLabBookServiceMutations.test_makedir 1'] = {
    'data': {
        'makeLabbookDirectory': {
            'newLabbookFileEdge': {
                'node': {
                    'isDir': True,
                    'key': 'new_folder/',
                    'size': 4096
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

snapshots['TestLabBookServiceMutations.test_rename_labbook 2'] = {
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
                    'size': 4096
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
