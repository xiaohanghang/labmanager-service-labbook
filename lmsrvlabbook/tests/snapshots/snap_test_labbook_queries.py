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

snapshots['TestLabBookServiceQueries.test_list_files_code 1'] = {
    'data': {
        'labbook': {
            'code': {
                'files': {
                    'edges': [
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnNyYy8=',
                                'isDir': True,
                                'key': 'src/',
                                'size': 4096
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnRlc3RfZmlsZTEudHh0',
                                'isDir': False,
                                'key': 'test_file1.txt',
                                'size': 6
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnRlc3RfZmlsZTIudHh0',
                                'isDir': False,
                                'key': 'test_file2.txt',
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
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnNyYy9qcy8=',
                                'isDir': True,
                                'key': 'src/js/',
                                'size': 4096
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnNyYy90ZXN0LnB5',
                                'isDir': False,
                                'key': 'src/test.py',
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
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnNyYy9qcy8=',
                                'isDir': True,
                                'key': 'src/js/',
                                'size': 4096
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnNyYy90ZXN0LnB5',
                                'isDir': False,
                                'key': 'src/test.py',
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
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnRlc3RfZmlsZTEudHh0',
                                'isDir': False,
                                'key': 'test_file1.txt',
                                'size': 6
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnRlc3RfZmlsZTIudHh0',
                                'isDir': False,
                                'key': 'test_file2.txt',
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
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZpbnB1dCZzdWJkaXIv',
                                'isDir': True,
                                'key': 'subdir/',
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
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZvdXRwdXQmZW1wdHkv',
                                'isDir': True,
                                'key': 'empty/',
                                'size': 4096
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZvdXRwdXQmcmVzdWx0LmRhdA==',
                                'isDir': False,
                                'key': 'result.dat',
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
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnRlc3RfZmlsZTEudHh0',
                                'isDir': False,
                                'key': 'test_file1.txt',
                                'size': 6
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnRlc3RfZmlsZTIudHh0',
                                'isDir': False,
                                'key': 'test_file2.txt',
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
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZpbnB1dCZzdWJkaXIvZGF0YS5kYXQ=',
                                'isDir': False,
                                'key': 'subdir/data.dat',
                                'size': 12
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZpbnB1dCZzdWJkaXIvZGF0YS8=',
                                'isDir': True,
                                'key': 'subdir/data/',
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

snapshots['TestLabBookServiceQueries.test_walkdir 1'] = {
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

snapshots['TestLabBookServiceQueries.test_list_favorites 1'] = {
    'data': {
        'labbook': {
            'code': {
                'favorites': {
                    'edges': [
                        {
                            'node': {
                                'description': 'My file with stuff 1',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSYw',
                                'index': 0,
                                'isDir': False,
                                'key': 'test1.txt'
                            }
                        },
                        {
                            'node': {
                                'description': 'My file with stuff 2',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSYx',
                                'index': 1,
                                'isDir': False,
                                'key': 'test2.txt'
                            }
                        },
                        {
                            'node': {
                                'description': 'testing',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSYy',
                                'index': 2,
                                'isDir': True,
                                'key': 'blah/'
                            }
                        }
                    ]
                }
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_favorites 2'] = {
    'data': {
        'labbook': {
            'input': {
                'favorites': {
                    'edges': [
                        {
                            'node': {
                                'description': 'Data dir 1',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmaW5wdXQmMA==',
                                'index': 0,
                                'isDir': True,
                                'key': 'data1/'
                            }
                        }
                    ]
                }
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_favorites 3'] = {
    'data': {
        'labbook': {
            'name': 'labbook1',
            'output': {
                'favorites': {
                    'edges': [
                        {
                            'node': {
                                'description': 'Data dir 2',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmb3V0cHV0JjA=',
                                'index': 0,
                                'isDir': True,
                                'key': 'data2/'
                            }
                        }
                    ]
                }
            }
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_favorites 4'] = {
    'data': {
        'labbook': {
            'code': {
                'favorites': {
                    'edges': [
                        {
                            'node': {
                                'description': 'My file with stuff 1',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSYw',
                                'index': 0,
                                'isDir': False,
                                'key': 'test1.txt'
                            }
                        },
                        {
                            'node': {
                                'description': 'My file with stuff 2',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSYx',
                                'index': 1,
                                'isDir': False,
                                'key': 'test2.txt'
                            }
                        },
                        {
                            'node': {
                                'description': 'testing',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSYy',
                                'index': 2,
                                'isDir': True,
                                'key': 'blah/'
                            }
                        }
                    ]
                }
            },
            'input': {
                'favorites': {
                    'edges': [
                        {
                            'node': {
                                'description': 'Data dir 1',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmaW5wdXQmMA==',
                                'index': 0,
                                'isDir': True,
                                'key': 'data1/'
                            }
                        }
                    ]
                }
            },
            'name': 'labbook1',
            'output': {
                'favorites': {
                    'edges': [
                        {
                            'node': {
                                'description': 'Data dir 2',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmb3V0cHV0JjA=',
                                'index': 0,
                                'isDir': True,
                                'key': 'data2/'
                            }
                        }
                    ]
                }
            }
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_favorite_and_files 1'] = {
    'data': {
        'labbook': {
            'code': {
                'favorites': {
                    'edges': [
                        {
                            'node': {
                                'description': 'My file with stuff 2',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSYw',
                                'index': 0,
                                'isDir': False,
                                'key': 'test2.txt'
                            }
                        },
                        {
                            'node': {
                                'description': 'testing',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSYx',
                                'index': 1,
                                'isDir': True,
                                'key': 'blah/'
                            }
                        }
                    ]
                },
                'files': {
                    'edges': [
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJmJsYWgv',
                                'isDir': True,
                                'key': 'blah/',
                                'size': 4096
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnRlc3QxLnR4dA==',
                                'isDir': False,
                                'key': 'test1.txt',
                                'size': 5
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnRlc3QyLnR4dA==',
                                'isDir': False,
                                'key': 'test2.txt',
                                'size': 5
                            }
                        }
                    ]
                }
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_all_files_many 1'] = {
    'data': {
        'labbook': {
            'code': {
                'allFiles': {
                    'edges': [
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnRlc3RfZmlsZTEudHh0',
                                'isDir': False,
                                'key': 'test_file1.txt',
                                'size': 6
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnRlc3RfZmlsZTIudHh0',
                                'isDir': False,
                                'key': 'test_file2.txt',
                                'size': 15
                            }
                        }
                    ]
                }
            },
            'input': {
                'allFiles': {
                    'edges': [
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZpbnB1dCZzdWJkaXIv',
                                'isDir': True,
                                'key': 'subdir/',
                                'size': 4096
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZpbnB1dCZzdWJkaXIvZGF0YS8=',
                                'isDir': True,
                                'key': 'subdir/data/',
                                'size': 4096
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZpbnB1dCZzdWJkaXIvZGF0YS5kYXQ=',
                                'isDir': False,
                                'key': 'subdir/data.dat',
                                'size': 12
                            }
                        }
                    ]
                }
            },
            'name': 'labbook1',
            'output': {
                'allFiles': {
                    'edges': [
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZvdXRwdXQmZW1wdHkv',
                                'isDir': True,
                                'key': 'empty/',
                                'size': 4096
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZvdXRwdXQmcmVzdWx0LmRhdA==',
                                'isDir': False,
                                'key': 'result.dat',
                                'size': 3
                            }
                        }
                    ]
                }
            }
        }
    }
}

snapshots['TestLabBookServiceQueries.test_get_activity_records 1'] = {
    'data': {
        'labbook': {
            'activityRecords': {
                'edges': [
                    {
                        'node': {
                            'importance': 255,
                            'message': 'Added new Output Data file /test_file.txt',
                            'show': True,
                            'tags': [
                                '.txt'
                            ],
                            'type': 'OUTPUT_DATA'
                        }
                    }
                ],
                'pageInfo': {
                    'hasNextPage': True,
                    'hasPreviousPage': False
                }
            },
            'description': 'my test description',
            'name': 'labbook11'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_get_activity_records 2'] = {
    'data': {
        'labbook': {
            'activityRecords': {
                'edges': [
                    {
                        'node': {
                            'importance': 255,
                            'message': 'Added new Input Data file /test_file.txt',
                            'show': True,
                            'tags': [
                                '.txt'
                            ],
                            'type': 'INPUT_DATA'
                        }
                    },
                    {
                        'node': {
                            'importance': 255,
                            'message': 'Added new Code file /test_file.txt',
                            'show': True,
                            'tags': [
                                '.txt'
                            ],
                            'type': 'CODE'
                        }
                    }
                ],
                'pageInfo': {
                    'hasNextPage': True,
                    'hasPreviousPage': False
                }
            },
            'description': 'my test description',
            'name': 'labbook11'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_get_activity_records 3'] = {
    'data': {
        'labbook': {
            'activityRecords': {
                'edges': [
                    {
                        'node': {
                            'importance': 255,
                            'message': 'Created new LabBook: default/labbook11',
                            'show': True,
                            'tags': None,
                            'type': 'LABBOOK'
                        }
                    }
                ],
                'pageInfo': {
                    'hasNextPage': False,
                    'hasPreviousPage': False
                }
            },
            'description': 'my test description',
            'name': 'labbook11'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_get_activity_records 4'] = {
    'data': {
        'labbook': {
            'activityRecords': {
                'edges': [
                ],
                'pageInfo': {
                    'hasNextPage': False,
                    'hasPreviousPage': False
                }
            },
            'description': 'my test description',
            'name': 'labbook11'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_get_activity_records_reverse_error 1'] = {
    'data': {
        'labbook': {
            'activityRecords': None,
            'description': 'my first labbook1',
            'name': 'labbook12'
        }
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 6
                }
            ],
            'message': 'Only `after` and `first` arguments are supported when paging activity records'
        }
    ]
}

snapshots['TestLabBookServiceQueries.test_get_activity_records_reverse_error 2'] = {
    'data': {
        'labbook': {
            'activityRecords': None,
            'description': 'my first labbook1',
            'name': 'labbook12'
        }
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 6
                }
            ],
            'message': 'Only `after` and `first` arguments are supported when paging activity records'
        }
    ]
}

snapshots['TestLabBookServiceQueries.test_get_activity_records_reverse_error 3'] = {
    'data': {
        'labbook': {
            'activityRecords': None,
            'description': 'my first labbook1',
            'name': 'labbook12'
        }
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 6
                }
            ],
            'message': 'Only `after` and `first` arguments are supported when paging activity records'
        }
    ]
}

snapshots['TestLabBookServiceQueries.test_get_activity_records_with_details 1'] = {
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
                                            'Added new Output Data file /test_file.txt'
                                        ]
                                    ],
                                    'importance': 0,
                                    'show': False,
                                    'tags': [
                                    ],
                                    'type': 'OUTPUT_DATA'
                                }
                            ],
                            'importance': 255,
                            'message': 'Added new Output Data file /test_file.txt',
                            'show': True,
                            'tags': [
                                '.txt'
                            ],
                            'type': 'OUTPUT_DATA'
                        }
                    },
                    {
                        'node': {
                            'detailObjects': [
                                {
                                    'data': [
                                        [
                                            'text/plain',
                                            'Added new Input Data file /test_file.txt'
                                        ]
                                    ],
                                    'importance': 0,
                                    'show': False,
                                    'tags': [
                                    ],
                                    'type': 'INPUT_DATA'
                                }
                            ],
                            'importance': 255,
                            'message': 'Added new Input Data file /test_file.txt',
                            'show': True,
                            'tags': [
                                '.txt'
                            ],
                            'type': 'INPUT_DATA'
                        }
                    },
                    {
                        'node': {
                            'detailObjects': [
                                {
                                    'data': [
                                        [
                                            'text/plain',
                                            'Added new Code file /test_file.txt'
                                        ]
                                    ],
                                    'importance': 0,
                                    'show': False,
                                    'tags': [
                                    ],
                                    'type': 'CODE'
                                }
                            ],
                            'importance': 255,
                            'message': 'Added new Code file /test_file.txt',
                            'show': True,
                            'tags': [
                                '.txt'
                            ],
                            'type': 'CODE'
                        }
                    },
                    {
                        'node': {
                            'detailObjects': [
                                {
                                    'data': [
                                        [
                                            'text/plain',
                                            'Created new LabBook: default/labbook11'
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
                            'message': 'Created new LabBook: default/labbook11',
                            'show': True,
                            'tags': None,
                            'type': 'LABBOOK'
                        }
                    }
                ]
            },
            'description': 'my test description',
            'name': 'labbook11'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_get_detail_record 1'] = {
    'data': {
        'labbook': {
            'description': 'my test description',
            'detailRecord': {
                'data': [
                    [
                        'text/plain',
                        'Created new LabBook: default/labbook11'
                    ]
                ],
                'importance': 0,
                'show': False,
                'tags': [
                ],
                'type': 'LABBOOK'
            },
            'name': 'labbook11'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_get_detail_record 2'] = {
    'data': {
        'labbook': {
            'description': 'my test description',
            'detailRecord': {
                'data': [
                    [
                        'text/plain',
                        'Added new Code file /test_file.txt'
                    ]
                ],
                'importance': 0,
                'show': False,
                'tags': [
                ],
                'type': 'CODE'
            },
            'name': 'labbook11'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_get_detail_records 1'] = {
    'data': {
        'labbook': {
            'description': 'my test description',
            'detailRecords': [
                {
                    'data': [
                        [
                            'text/plain',
                            'Created new LabBook: default/labbook11'
                        ]
                    ],
                    'importance': 0,
                    'show': False,
                    'tags': [
                    ],
                    'type': 'LABBOOK'
                },
                {
                    'data': [
                        [
                            'text/plain',
                            'Added new Code file /test_file.txt'
                        ]
                    ],
                    'importance': 0,
                    'show': False,
                    'tags': [
                    ],
                    'type': 'CODE'
                }
            ],
            'name': 'labbook11'
        }
    }
}
