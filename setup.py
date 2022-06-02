"""Sets up the package"""

#!/usr/bin/env python
 # -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

with open('README.md') as f:
    README = f.read()

with open('LICENSE.md') as f:
    LICENSE = f.read()

setup(
    name='floralapp',
    version='0.1.0',
    description='Floral Budgeting Tool application',
    long_description=README,
    author='katherine-kania',
    author_email='<email>',
    url='https://github.com/katherine-kania/flower-budgeting-api',
    license=LICENSE,
    packages=find_packages(exclude=('tests', 'docs'))
)
