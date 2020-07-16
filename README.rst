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

me4cli - EXAMPLE USAGE
======================

.. code-block:: bash

  # Create a config file for the API password (or enter this in the cli)
  $ cat .me4cli.conf
  [API]
  api_baseurl = https://localhost
  api_port = 9446
  api_username = manage
  api_password = changeme
  api_disable_tls_verification = True


.. code-block:: bash

  $ me4cli -f .me4cli.conf show system-info
  System: array-name
    Product Type:    ME4084
    Contact:         root@example.com
    Description:     array-description
    Location:        array-location

  Service Tags:
    Enclosure 0:     LKJD873

  NTP:
    Status:          activated
    Server:          192.168.1.254
    Time (UTC):      2020-03-01 16:11:05

CLI Help page:

.. code-block:: bash

   $ me4cli --help
   usage: me4cli [-h] [-f [CONFIG_FILES]] [--debug] [--quiet] [--nocolour]
                 {check,set,show} ...

   optional arguments:
     -h, --help            show this help message and exit
     -f [CONFIG_FILES], --config-files [CONFIG_FILES]
                           Tool configuration file location (default:
                           ['/etc/me4cli/me4cli.conf', '.me4cli.conf'])
     --debug               Enable debug output
     --quiet               Suppress all informational output, log at WARN level
     --nocolour, --nocolor
                           Strip ANSI color codes from all output to console

   subcommands:
     Below are the core subcommands of program:

     {check,set,show}
       check               check commands
       set                 set commands
       show                show commands

Example Array Setup
===================

.. code-block:: bash

  (me4storage) [matt@yoshimo]:me4storage/ (master *%>) $ me4cli -f .me4cli.conf.rds-ost-jb52 delete host-configuration
  [INFO] Found configuration files: ['.me4cli.conf.rds-ost-jb52']
  [INFO] Deleting all host groups present...
  [INFO] Deleting all initiator nicknames...

  (me4storage) [matt@yoshimo]:me4storage/ (master *%>) $ me4cli -f .me4cli.conf.rds-ost-jb52 configure host rds-oss51 --port-wwpn 0x54cd98f0c83fbe00 0x54cd98f0c83ffe00
  [INFO] Found configuration files: ['.me4cli.conf.rds-ost-jb52']
  [INFO] Setting initiator nickname: rds-oss51-P0 to 54cd98f0c83fbe00
  [INFO] Setting initiator nickname: rds-oss51-P1 to 54cd98f0c83ffe00
  [INFO] Creating host: rds-oss51...
  [INFO] Creating host group: hg-rds-ost-jb52...

  (me4storage) [matt@yoshimo]:me4storage/ (master *%>) $ me4cli -f .me4cli.conf.rds-ost-jb52 configure host rds-oss52 --port-wwpn 0x54cd98f0c83ed500 0x54cd98f0c83faf00
  [INFO] Found configuration files: ['.me4cli.conf.rds-ost-jb52']
  [INFO] Setting initiator nickname: rds-oss52-P0 to 54cd98f0c83ed500
  [INFO] Setting initiator nickname: rds-oss52-P1 to 54cd98f0c83faf00
  [INFO] Creating host: rds-oss52...
  [INFO] Adding rds-oss52 to host group: hg-rds-ost-jb52...
