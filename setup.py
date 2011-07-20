#!/usr/bin/env python

"""JSON Requestor"""

from setuptools import setup, find_packages

setup(
    name = 'jsonrequester',
    version = '0.1.0',
    description = 'A library for client JSON REST requests',
    packages = find_packages(),
    install_requires=[
        'httplib2',
    ],
    test_suite = 'tests',
)
