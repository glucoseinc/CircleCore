#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup
import sys


PY2 = sys.version_info[0] == 2


install_requires = [
    'base58',
    'click>=6',
    'flask',
    'nnpy',
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
    ],
    entry_points={
        'console_scripts': [
            'crcr=circle_core.cli:cli_entry',
        ],
    },
)
