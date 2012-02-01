#!/usr/bin/env python
"""JSON Requestor"""
import os

from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'jsonrequester',
    version = '0.1.5',
    description = 'A library for client JSON REST requests',
    packages = find_packages(),
    long_description=read('README.rst'),
    install_requires=[
        'httplib2',
    ],
    test_suite = 'tests',
)
