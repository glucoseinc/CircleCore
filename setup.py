#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name='CircleCore',
    version='0.1',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'click>=6',
        'flask',
        'nnpy',
        'redis',
        'six',
        'tornado',
        'websocket-client',
    ],
    dependency_links=[
        'git+https://github.com/nanomsg/nnpy.git#egg=nnpy',
    ],
    entry_points={
        'console_scripts': [
            'crcr=circle_core.cli:cli_main',
        ],
    },
)
