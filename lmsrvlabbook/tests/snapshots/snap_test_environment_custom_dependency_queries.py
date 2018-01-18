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
                        'componentId': 'pillow',
                        'description': 'Pillow v4.2.1 for Ubuntu and Python3',
                        'dockerSnippet': '''RUN apt-get -y install libjpeg-dev libtiff5-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjpeg-dev
RUN pip3 install Pillow==4.2.1 
''',
                        'id': 'Q3VzdG9tQ29tcG9uZW50OmdpZy1kZXZfY29tcG9uZW50czImcGlsbG93JjA=',
                        'license': None,
                        'name': 'Pillow',
                        'repository': 'gig-dev_components2',
                        'requiredPackageManagers': None,
                        'revision': 0,
                        'tags': [
                            'ubuntu',
                            'python',
                            'python3',
                            'image',
                            'jpeg',
                            'png'
                        ],
                        'url': None
                    }
                }
            ]
        }
    }
}
