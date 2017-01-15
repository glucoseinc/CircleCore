#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup
import sys


PY2 = sys.version_info[0] == 2


install_requires = [
    'base58',
    'click>=6',
    'flask',
    'Flask-OAuthlib',
    'nnpy',
    'python-dateutil',
    'redis',
    'six',
    'sqlalchemy>=1.1.4',
    'tornado',
    'websocket-client',
]
if PY2:
    install_requires.append('enum34')


setup(
    name='CircleCore',
    version='0.1',
    packages=find_packages(exclude=['tests']),
    install_requires=install_requires,
    dependency_links=[
        'git+https://github.com/nanomsg/nnpy.git#egg=nnpy',
        # 'git+https://github.com/mysql/mysql-connector-python.git@2.2.1-m2#egg=mysql-connector-python',
        # 'http://cdn.mysql.com//Downloads/Connector-Python/mysql-connector-python-2.2.1.tar.gz'
    ],
    entry_points={
        'console_scripts': [
            'crcr=circle_core.cli:cli_entry',
        ],
    },
    extras_require={
        'test': [
            'coverage',
            'flake8',
            'flake8-import-order',
            'nnpy',
            'pytest',
            'pytest-timeout',
            'tcptest',
            'tox',
        ],
        'redis': [
            'redis',
        ],
        'mysql': [
            'mysql-connector-python>=2.2.1',
        ]
    }
)
