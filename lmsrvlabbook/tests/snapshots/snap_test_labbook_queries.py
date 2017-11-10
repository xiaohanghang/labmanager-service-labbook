# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestLabBookServiceQueries.test_list_labbooks 1'] = {
    'data': {
        'localLabbooks': {
            'edges': [
                {
                    'cursor': 'MA==',
                    'node': {
                        'description': 'my first labbook1',
                        'name': 'labbook1'
                    }
                },
                {
                    'cursor': 'MQ==',
                    'node': {
                        'description': 'my first labbook2',
                        'name': 'labbook2'
                    }
                }
            ]
        }
    }
}

snapshots['TestLabBookServiceQueries.test_pagination_noargs 1'] = {
    'data': {
        'localLabbooks': {
            'edges': [
                {
                    'cursor': 'MA==',
                    'node': {
                        'description': 'Cats labbook 1',
                        'name': 'labbook1'
                    }
                },
                {
                    'cursor': 'MQ==',
                    'node': {
                        'description': 'Dogs labbook 2',
                        'name': 'labbook2'
                    }
                },
                {
                    'cursor': 'Mg==',
                    'node': {
                        'description': 'Mice labbook 3',
                        'name': 'labbook3'
                    }
                },
                {
                    'cursor': 'Mw==',
                    'node': {
                        'description': 'Horses labbook 4',
                        'name': 'labbook4'
                    }
                },
                {
                    'cursor': 'NA==',
                    'node': {
                        'description': 'Cheese labbook 5',
                        'name': 'labbook5'
                    }
                },
                {
                    'cursor': 'NQ==',
                    'node': {
                        'description': 'Goat labbook 6',
                        'name': 'labbook6'
                    }
                },
                {
                    'cursor': 'Ng==',
                    'node': {
                        'description': 'Turtle labbook 7',
                        'name': 'labbook7'
                    }
                },
                {
                    'cursor': 'Nw==',
                    'node': {
                        'description': 'Lamb labbook 8',
                        'name': 'labbook8'
                    }
                },
                {
                    'cursor': 'OA==',
                    'node': {
                        'description': 'Taco labbook 9',
                        'name': 'labbook9'
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

snapshots['TestLabBookServiceQueries.test_pagination_first_only 1'] = {
    'data': {
        'localLabbooks': {
            'edges': [
                {
                    'cursor': 'MA==',
                    'node': {
                        'description': 'Cats labbook 1',
                        'name': 'labbook1'
                    }
                },
                {
                    'cursor': 'MQ==',
                    'node': {
                        'description': 'Dogs labbook 2',
                        'name': 'labbook2'
                    }
                },
                {
                    'cursor': 'Mg==',
                    'node': {
                        'description': 'Mice labbook 3',
                        'name': 'labbook3'
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

snapshots['TestLabBookServiceQueries.test_pagination_first_and_after 1'] = {
    'data': {
        'localLabbooks': {
            'edges': [
                {
                    'cursor': 'Mw==',
                    'node': {
                        'description': 'Horses labbook 4',
                        'name': 'labbook4'
                    }
                },
                {
                    'cursor': 'NA==',
                    'node': {
                        'description': 'Cheese labbook 5',
                        'name': 'labbook5'
                    }
                },
                {
                    'cursor': 'NQ==',
                    'node': {
                        'description': 'Goat labbook 6',
                        'name': 'labbook6'
                    }
                },
                {
                    'cursor': 'Ng==',
                    'node': {
                        'description': 'Turtle labbook 7',
                        'name': 'labbook7'
                    }
                }
            ],
            'pageInfo': {
                'endCursor': 'Ng==',
                'hasNextPage': True,
                'hasPreviousPage': False,
                'startCursor': 'Mw=='
            }
        }
    }
}

snapshots['TestLabBookServiceQueries.test_pagination_first_and_after 2'] = {
    'data': {
        'localLabbooks': {
            'edges': [
                {
                    'cursor': 'Nw==',
                    'node': {
                        'description': 'Lamb labbook 8',
                        'name': 'labbook8'
                    }
                },
                {
                    'cursor': 'OA==',
                    'node': {
                        'description': 'Taco labbook 9',
                        'name': 'labbook9'
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

snapshots['TestLabBookServiceQueries.test_pagination_first_and_after 3'] = {
    'data': {
        'localLabbooks': {
            'edges': [
            ],
            'pageInfo': {
                'hasNextPage': False,
                'hasPreviousPage': False
            }
        }
    }
}

snapshots['TestLabBookServiceQueries.test_pagination_last_only 1'] = {
    'data': {
        'localLabbooks': {
            'edges': [
                {
                    'cursor': 'Ng==',
                    'node': {
                        'description': 'Turtle labbook 7',
                        'name': 'labbook7'
                    }
                },
                {
                    'cursor': 'Nw==',
                    'node': {
                        'description': 'Lamb labbook 8',
                        'name': 'labbook8'
                    }
                },
                {
                    'cursor': 'OA==',
                    'node': {
                        'description': 'Taco labbook 9',
                        'name': 'labbook9'
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

snapshots['TestLabBookServiceQueries.test_pagination_last_and_before 1'] = {
    'data': {
        'localLabbooks': {
            'edges': [
                {
                    'cursor': 'NA==',
                    'node': {
                        'description': 'Cheese labbook 5',
                        'name': 'labbook5'
                    }
                },
                {
                    'cursor': 'NQ==',
                    'node': {
                        'description': 'Goat labbook 6',
                        'name': 'labbook6'
                    }
                },
                {
                    'cursor': 'Ng==',
                    'node': {
                        'description': 'Turtle labbook 7',
                        'name': 'labbook7'
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

snapshots['TestLabBookServiceQueries.test_pagination_last_and_before 2'] = {
    'data': {
        'localLabbooks': {
            'edges': [
                {
                    'cursor': 'MA==',
                    'node': {
                        'description': 'Cats labbook 1',
                        'name': 'labbook1'
                    }
                }
            ],
            'pageInfo': {
                'endCursor': 'MA==',
                'hasNextPage': False,
                'hasPreviousPage': False,
                'startCursor': 'MA=='
            }
        }
    }
}

snapshots['TestLabBookServiceQueries.test_pagination_last_and_before 3'] = {
    'data': {
        'localLabbooks': {
            'edges': [
            ],
            'pageInfo': {
                'endCursor': None,
                'hasNextPage': False,
                'hasPreviousPage': False,
                'startCursor': None
            }
        }
    }
}

snapshots['TestLabBookServiceQueries.test_pagination 1'] = {
    'data': {
        'localLabbooks': {
            'edges': [
                {
                    'cursor': 'Mg==',
                    'node': {
                        'description': 'Mice labbook 3',
                        'name': 'labbook3'
                    }
                },
                {
                    'cursor': 'Mw==',
                    'node': {
                        'description': 'Horses labbook 4',
                        'name': 'labbook4'
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

snapshots['TestLabBookServiceQueries.test_pagination 2'] = {
    'data': {
        'localLabbooks': {
            'edges': [
                {
                    'cursor': 'NA==',
                    'node': {
                        'description': 'Cheese labbook 5',
                        'name': 'labbook5'
                    }
                },
                {
                    'cursor': 'NQ==',
                    'node': {
                        'description': 'Goat labbook 6',
                        'name': 'labbook6'
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

snapshots['TestLabBookServiceQueries.test_get_labbook 1'] = {
    'data': {
        'labbook': {
            'activeBranch': {
                'name': 'master'
            },
            'description': 'my first labbook1',
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_labbooks_container_status 1'] = {
    'data': {
        'localLabbooks': {
            'edges': [
                {
                    'cursor': 'MA==',
                    'node': {
                        'description': 'my first labbook1',
                        'environment': {
                            'containerStatus': 'NOT_RUNNING',
                            'imageStatus': 'DOES_NOT_EXIST'
                        },
                        'name': 'labbook1'
                    }
                },
                {
                    'cursor': 'MQ==',
                    'node': {
                        'description': 'my first labbook2',
                        'environment': {
                            'containerStatus': 'NOT_RUNNING',
                            'imageStatus': 'DOES_NOT_EXIST'
                        },
                        'name': 'labbook2'
                    }
                }
            ]
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_labbooks_container_status_no_labbooks 1'] = {
    'data': {
        'localLabbooks': {
            'edges': [
            ]
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_favorites 1'] = {
    'data': {
        'labbook': {
            'favorites': {
                'edges': [
                    {
                        'node': {
                            'description': 'My file with stuff 1',
                            'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmZGVmYXVsdCZsYWJib29rMSZjb2RlJjA=',
                            'index': 0,
                            'isDir': False,
                            'key': 'code/test1.txt'
                        }
                    },
                    {
                        'node': {
                            'description': 'My file with stuff 2',
                            'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmZGVmYXVsdCZsYWJib29rMSZjb2RlJjE=',
                            'index': 1,
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

snapshots['TestLabBookServiceQueries.test_list_favorites 2'] = {
    'data': {
        'labbook': {
            'favorites': {
                'edges': [
                    {
                        'node': {
                            'description': 'Data dir 1',
                            'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmZGVmYXVsdCZsYWJib29rMSZpbnB1dCYw',
                            'index': 0,
                            'isDir': True,
                            'key': 'input/data1/'
                        }
                    }
                ]
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_favorites 3'] = {
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

snapshots['TestLabBookServiceQueries.test_listdir 1'] = {
    'data': {
        'labbook': {
            'files': {
                'edges': [
                    {
                        'node': {
                            'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JmxhYmJvb2sxJmNvZGUv',
                            'isDir': True,
                            'key': 'code/',
                            'size': 4096
                        }
                    },
                    {
                        'node': {
                            'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JmxhYmJvb2sxJmlucHV0Lw==',
                            'isDir': True,
                            'key': 'input/',
                            'size': 4096
                        }
                    },
                    {
                        'node': {
                            'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JmxhYmJvb2sxJm91dHB1dC8=',
                            'isDir': True,
                            'key': 'output/',
                            'size': 4096
                        }
                    }
                ]
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_files 1'] = {
    'data': {
        'labbook': {
            'files': {
                'edges': [
                    {
                        'node': {
                            'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JmxhYmJvb2sxJmNvZGUv',
                            'isDir': True,
                            'key': 'code/',
                            'size': 4096
                        }
                    },
                    {
                        'node': {
                            'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JmxhYmJvb2sxJmNvZGUvdGVzdF9maWxlMS50eHQ=',
                            'isDir': False,
                            'key': 'code/test_file1.txt',
                            'size': 6
                        }
                    },
                    {
                        'node': {
                            'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JmxhYmJvb2sxJmNvZGUvdGVzdF9maWxlMi50eHQ=',
                            'isDir': False,
                            'key': 'code/test_file2.txt',
                            'size': 6
                        }
                    },
                    {
                        'node': {
                            'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JmxhYmJvb2sxJmlucHV0Lw==',
                            'isDir': True,
                            'key': 'input/',
                            'size': 4096
                        }
                    },
                    {
                        'node': {
                            'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JmxhYmJvb2sxJm91dHB1dC8=',
                            'isDir': True,
                            'key': 'output/',
                            'size': 4096
                        }
                    }
                ]
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_subfolder_files 1'] = {
    'data': {
        'labbook': {
            'codeFiles': {
                'edges': [
                    {
                        'node': {
                            'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JnRlc3QtbGFiYm9vayZjb2RlL2NvZGVfZmlsZS50eHQ=',
                            'isDir': False,
                            'key': 'code/code_file.txt',
                            'size': 6
                        }
                    }
                ]
            },
            'files': {
                'edges': [
                    {
                        'node': {
                            'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JnRlc3QtbGFiYm9vayZjb2RlLw==',
                            'isDir': True,
                            'key': 'code/',
                            'size': 4096
                        }
                    },
                    {
                        'node': {
                            'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JnRlc3QtbGFiYm9vayZjb2RlL2NvZGVfZmlsZS50eHQ=',
                            'isDir': False,
                            'key': 'code/code_file.txt',
                            'size': 6
                        }
                    },
                    {
                        'node': {
                            'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JnRlc3QtbGFiYm9vayZpbnB1dC8=',
                            'isDir': True,
                            'key': 'input/',
                            'size': 4096
                        }
                    },
                    {
                        'node': {
                            'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JnRlc3QtbGFiYm9vayZpbnB1dC9pbnB1dF9maWxlLnR4dA==',
                            'isDir': False,
                            'key': 'input/input_file.txt',
                            'size': 6
                        }
                    },
                    {
                        'node': {
                            'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JnRlc3QtbGFiYm9vayZvdXRwdXQv',
                            'isDir': True,
                            'key': 'output/',
                            'size': 4096
                        }
                    },
                    {
                        'node': {
                            'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JnRlc3QtbGFiYm9vayZvdXRwdXQvb3V0cHV0X2ZpbGUudHh0',
                            'isDir': False,
                            'key': 'output/output_file.txt',
                            'size': 6
                        }
                    }
                ]
            },
            'inputFiles': {
                'edges': [
                    {
                        'node': {
                            'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JnRlc3QtbGFiYm9vayZpbnB1dC9pbnB1dF9maWxlLnR4dA==',
                            'isDir': False,
                            'key': 'input/input_file.txt',
                            'size': 6
                        }
                    }
                ]
            },
            'name': 'test-labbook',
            'outputFiles': {
                'edges': [
                    {
                        'node': {
                            'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JnRlc3QtbGFiYm9vayZvdXRwdXQvb3V0cHV0X2ZpbGUudHh0',
                            'isDir': False,
                            'key': 'output/output_file.txt',
                            'size': 6
                        }
                    }
                ]
            }
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_files_code 1'] = {
    'data': {
        'labbook': {
            'code': {
                'files': {
                    'edges': [
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JmxhYmJvb2sxJmNvZGUvc3JjLw==',
                                'isDir': True,
                                'key': 'code/src/',
                                'size': 4096
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JmxhYmJvb2sxJmNvZGUvdGVzdF9maWxlMS50eHQ=',
                                'isDir': False,
                                'key': 'code/test_file1.txt',
                                'size': 6
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JmxhYmJvb2sxJmNvZGUvdGVzdF9maWxlMi50eHQ=',
                                'isDir': False,
                                'key': 'code/test_file2.txt',
                                'size': 15
                            }
                        }
                    ]
                }
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_files_code 2'] = {
    'data': {
        'labbook': {
            'code': {
                'files': {
                    'edges': [
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JmxhYmJvb2sxJmNvZGUvc3JjL2pzLw==',
                                'isDir': True,
                                'key': 'code/src/js/',
                                'size': 4096
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JmxhYmJvb2sxJmNvZGUvc3JjL3Rlc3QucHk=',
                                'isDir': False,
                                'key': 'code/src/test.py',
                                'size': 21
                            }
                        }
                    ]
                }
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_files_code 3'] = {
    'data': {
        'labbook': {
            'code': {
                'files': {
                    'edges': [
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JmxhYmJvb2sxJmNvZGUvc3JjL2pzLw==',
                                'isDir': True,
                                'key': 'code/src/js/',
                                'size': 4096
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JmxhYmJvb2sxJmNvZGUvc3JjL3Rlc3QucHk=',
                                'isDir': False,
                                'key': 'code/src/test.py',
                                'size': 21
                            }
                        }
                    ]
                }
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_files_many 1'] = {
    'data': {
        'labbook': {
            'code': {
                'files': {
                    'edges': [
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JmxhYmJvb2sxJmNvZGUvdGVzdF9maWxlMS50eHQ=',
                                'isDir': False,
                                'key': 'code/test_file1.txt',
                                'size': 6
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JmxhYmJvb2sxJmNvZGUvdGVzdF9maWxlMi50eHQ=',
                                'isDir': False,
                                'key': 'code/test_file2.txt',
                                'size': 15
                            }
                        }
                    ]
                }
            },
            'input': {
                'files': {
                    'edges': [
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JmxhYmJvb2sxJmlucHV0L3N1YmRpci8=',
                                'isDir': True,
                                'key': 'input/subdir/',
                                'size': 4096
                            }
                        }
                    ]
                }
            },
            'name': 'labbook1',
            'output': {
                'files': {
                    'edges': [
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JmxhYmJvb2sxJm91dHB1dC9lbXB0eS8=',
                                'isDir': True,
                                'key': 'output/empty/',
                                'size': 4096
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JmxhYmJvb2sxJm91dHB1dC9yZXN1bHQuZGF0',
                                'isDir': False,
                                'key': 'output/result.dat',
                                'size': 3
                            }
                        }
                    ]
                }
            }
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_files_many 2'] = {
    'data': {
        'labbook': {
            'code': {
                'files': {
                    'edges': [
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JmxhYmJvb2sxJmNvZGUvdGVzdF9maWxlMS50eHQ=',
                                'isDir': False,
                                'key': 'code/test_file1.txt',
                                'size': 6
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JmxhYmJvb2sxJmNvZGUvdGVzdF9maWxlMi50eHQ=',
                                'isDir': False,
                                'key': 'code/test_file2.txt',
                                'size': 15
                            }
                        }
                    ]
                }
            },
            'input': {
                'files': {
                    'edges': [
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JmxhYmJvb2sxJmlucHV0L3N1YmRpci9kYXRhLmRhdA==',
                                'isDir': False,
                                'key': 'input/subdir/data.dat',
                                'size': 12
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JmxhYmJvb2sxJmlucHV0L3N1YmRpci9kYXRhLw==',
                                'isDir': True,
                                'key': 'input/subdir/data/',
                                'size': 4096
                            }
                        }
                    ]
                }
            },
            'name': 'labbook1',
            'output': {
                'files': {
                    'edges': [
                    ]
                }
            }
        }
    }
}
