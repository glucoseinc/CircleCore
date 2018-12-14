#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

install_requires = [
    'alembic',
    'asyncio_extras',
    'base58',
    'click>=6',
    'Flask>=0.11',
    'Flask-OAuthlib',
    'mysql-connector-python-rf',
    'nnpy==1.4.2',
    'python-dateutil',
    'sqlalchemy>=1.1.4',
    'typing_extension'
    'tornado',
    'websocket-client',
    'whisper==1.1.2',
]

setup(
    name='circle_core',
    version='0.1',
    packages=find_packages(exclude=['tests']),
    install_requires=install_requires,
    dependency_links=[],
    entry_points={
        'console_scripts': [
            'crcr=circle_core.cli:cli_entry',
        ],
    },
    extras_require={
        'test': [
            'autopep8',
            'coverage',
            'flake8',
            'flake8-import-order',
            'mypy',
            'pytest',
            'pytest-asyncio',
            'pytest-cov',
            'pytest-timeout',
            'tcptest',
            'tox',
            'yapf',
        ],
        'doc': [
            'Sphinx',
            'sphinx-rtd-theme',
        ]
    }
)
