# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestAddComponentMutations.test_add_package 1'] = {
    'data': {
        'addPackageComponent': {
            'clientMutationId': None,
            'newPackageComponentEdge': {
                'node': {
                    'fromBase': False,
                    'id': 'UGFja2FnZUNvbXBvbmVudDphcHQmZG9ja2VyJjEuMA==',
                    'manager': 'apt',
                    'package': 'docker',
                    'schema': 1,
                    'version': '1.0'
                }
            }
        }
    }
}

snapshots['TestAddComponentMutations.test_add_custom_dep 1'] = {
    'data': {
        'addCustomComponent': {
            'clientMutationId': None,
            'newCustomComponentEdge': {
                'node': {
                    'componentId': 'pillow',
                    'description': 'Pillow v4.2.1 for Ubuntu and Python3',
                    'dockerSnippet': '''RUN apt-get -y install libjpeg-dev libtiff5-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjpeg-dev
RUN pip3 install Pillow==4.2.1
''',
                    'id': 'Q3VzdG9tQ29tcG9uZW50OmdpZy1kZXZfY29tcG9uZW50czImcGlsbG93JjA=',
                    'license': 'PIL Software License',
                    'name': 'Pillow',
                    'repository': 'gig-dev_components2',
                    'requiredPackageManagers': [
                        'apt',
                        'pip'
                    ],
                    'revision': 0,
                    'tags': [
                        'ubuntu',
                        'python',
                        'python3',
                        'image',
                        'jpeg',
                        'png'
                    ],
                    'url': 'http://pillow.readthedocs.io/en/4.2.1/'
                }
            }
        }
    }
}
