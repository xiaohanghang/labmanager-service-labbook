# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestLabBookServiceMutations.test_create_labbook 1'] = {
    'data': {
        'labbook': {
            'description': 'my test description',
            'name': 'test-lab-book1',
            'notes': {
                'edges': [
                    {
                        'node': {
                            'freeText': '',
                            'message': 'Created new LabBook: default/test-lab-book1'
                        }
                    }
                ]
            }
        }
    }
}

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

snapshots['TestLabBookServiceMutations.test_add_file_errors 1'] = {
    'data': {
        'addLabbookFile': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 11,
                    'line': 3
                }
            ],
            'message': 'No file newFile in request context'
        }
    ]
}

snapshots['TestLabBookServiceMutations.test_add_file_errors 2'] = {
    'data': {
        'addLabbookFile': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 11,
                    'line': 3
                }
            ],
            'message': 'Filename of request file and `file_path` do not match'
        }
    ]
}

snapshots['TestLabBookServiceMutations.test_add_favorite 1'] = {
    'data': {
        'labbook': {
            'favorites': {
                'edges': [
                ]
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
                    'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmZGVmYXVsdCZsYWJib29rMSZjb2RlJjA=',
                    'index': 0,
                    'isDir': False,
                    'key': 'code/test.txt'
                }
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_add_favorite 3'] = {
    'data': {
        'labbook': {
            'favorites': {
                'edges': [
                    {
                        'node': {
                            'description': 'my test favorite',
                            'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmZGVmYXVsdCZsYWJib29rMSZjb2RlJjA=',
                            'index': 0,
                            'isDir': False,
                            'key': 'code/test.txt'
                        }
                    }
                ]
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceMutations.test_add_favorite_at_index 1'] = {
    'data': {
        'labbook': {
            'favorites': {
                'edges': [
                ]
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
                    'key': 'code/test1.txt'
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
                    'key': 'code/test2.txt'
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
                    'key': 'code/test3.txt'
                }
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_add_favorite_at_index 5'] = {
    'data': {
        'labbook': {
            'favorites': {
                'edges': [
                    {
                        'node': {
                            'description': 'my test favorite 1',
                            'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmZGVmYXVsdCZsYWJib29rMSZjb2RlJjA=',
                            'index': 0,
                            'isDir': False,
                            'key': 'code/test1.txt'
                        }
                    },
                    {
                        'node': {
                            'description': 'my test favorite 3',
                            'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmZGVmYXVsdCZsYWJib29rMSZjb2RlJjE=',
                            'index': 1,
                            'isDir': False,
                            'key': 'code/test3.txt'
                        }
                    },
                    {
                        'node': {
                            'description': 'my test favorite 2',
                            'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmZGVmYXVsdCZsYWJib29rMSZjb2RlJjI=',
                            'index': 2,
                            'isDir': False,
                            'key': 'code/test2.txt'
                        }
                    }
                ]
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
                    'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmZGVmYXVsdCZsYWJib29rMSZjb2RlJjA=',
                    'index': 0,
                    'isDir': False,
                    'key': 'code/test.txt'
                }
            }
        }
    }
}

snapshots['TestLabBookServiceMutations.test_delete_favorite 2'] = {
    'data': {
        'labbook': {
            'favorites': {
                'edges': [
                    {
                        'node': {
                            'description': 'my test favorite',
                            'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmZGVmYXVsdCZsYWJib29rMSZjb2RlJjA=',
                            'index': 0,
                            'isDir': False,
                            'key': 'code/test.txt'
                        }
                    }
                ]
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
            'favorites': {
                'edges': [
                ]
            },
            'name': 'labbook1'
        }
    }
}
