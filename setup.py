#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys

from setuptools import find_packages, setup

# Package meta-data.
NAME = 'me4storage'
DESCRIPTION = 'Simple CLI utility for Dell ME4 Storage'
URL = 'https://gitlab.developers.cam.ac.uk/rcs/platforms/storage-services/me4storage'
EMAIL = 'mjr208@cam.ac.uk'
AUTHOR = 'Matt Rásó-Barnett'

# What packages are required for this module to be executed?
REQUIRED = [
    'argcomplete',
    'colorlog',
    'colorama',
    'requests',
    'packaging',
    'terminaltables',
    'pysftp',
    'fuzzywuzzy',
    'python-Levenshtein',
]

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.rst' is present in your MANIFEST.in file!
with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

# Load the package's __version__.py module as a dictionary.
about = {}
with open(os.path.join(here, 'me4storage', '__version__.py')) as f:
    exec(f.read(), about)

# Check if running under Gitlab CI Pipeline, if so, take version from
# CI commit tag. Otherwise, use value from __version__.py
if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
elif os.environ.get('CI_COMMIT_SHORT_SHA'):
    version = about['__version__'] + '.' + os.environ['CI_COMMIT_SHORT_SHA']
else:
    version = about['__version__']

setup(
    name=NAME,
    version=version,
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    license='MIT',
    packages=find_packages(exclude=('tests', 'docs')),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],
    entry_points={
        'console_scripts': [
            'me4cli = me4storage.cli:cli',
            ],
    },
    install_requires=REQUIRED,
    include_package_data=True,
)

