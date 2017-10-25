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
                            'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JmxhYmJvb2sxJmInZXlKclpYa2lPaUFpWTI5a1pTSXNJQ0pwYzE5a2FYSWlPaUIwY25WbExDQWljMmw2WlNJNklEUXdPVFlzSUNKdGIyUnBabWxsWkY5aGRDSTZJREUxTURnNU1ERXpNREV1TWpoOSc=',
                            'isDir': True,
                            'key': 'code',
                            'size': 4096
                        }
                    },
                    {
                        'node': {
                            'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JmxhYmJvb2sxJmInZXlKclpYa2lPaUFpYVc1d2RYUWlMQ0FpYVhOZlpHbHlJam9nZEhKMVpTd2dJbk5wZW1VaU9pQTBNRGsyTENBaWJXOWthV1pwWldSZllYUWlPaUF4TlRBNE9UQXhNekF4TGpJNGZRPT0n',
                            'isDir': True,
                            'key': 'input',
                            'size': 4096
                        }
                    },
                    {
                        'node': {
                            'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZkZWZhdWx0JmxhYmJvb2sxJmInZXlKclpYa2lPaUFpYjNWMGNIVjBJaXdnSW1selgyUnBjaUk2SUhSeWRXVXNJQ0p6YVhwbElqb2dOREE1Tml3Z0ltMXZaR2xtYVdWa1gyRjBJam9nTVRVd09Ea3dNVE13TVM0eU9IMD0n',
                            'isDir': True,
                            'key': 'output',
                            'size': 4096
                        }
                    }
                ]
            },
            'name': 'labbook1'
        }
    }
}
