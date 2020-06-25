ME4 Storage Manager
===================

This project aims to be a simple CLI utility to configure ME4 storage
using the ME4 REST API `ME4 CLI Manual <https://www.dell.com/support/manuals/uk/en/ukbsdt1/powervault-me4012/me4_series_cli_pub>`_

INSTALLATION
============

The project is written against python3. Newer python3 versions should
work, but haven't been tested against.

After cloning the source code, it is recommended to create a virtualenv
to install the package into, otherwise it will try to install into your
global python environment.::

  mkvirtualenv -r requirements.txt --python python3.8 storage-automation

Once inside a virtualenv, install the application for development with::

  python setup.py develop

You should then have the CLI utility available in your
virtualenv::

  me4storage --help


You can also install the project dependencies with Pipenv:
https://github.com/pypa/pipenv ::

  pipenv --python 3.8
  pipenv install
  pipenv shell

me4storage - EXAMPLE USAGE
========================

.. code-block:: bash

  # Create a config file for the API password (or enter this in the cli)
  [mjr208@gw01]:~/ $ cat .me4storage.conf
  [Auth]
  api_user = manage
  api_password = [REDACTED]

