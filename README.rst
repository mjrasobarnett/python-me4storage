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
  api_host = localhost
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

A freshly delivered ME4 array from the factory will have a hardcoded IP
of 10.0.0.2 on it's management ports, and have no user configured.

First we need to connect to the array over this IP and set up an initial
user,

.. code-block:: bash

  $ cat .me4cli.conf.unconfigured
  [API]
  api_username = setup
  api_disable_tls_verification = True

  $ me4cli -f .me4cli.conf.unconfigured add user --api-host 10.0.0.2 --username manage --password XXXXXXXXX --roles manage monitor

Next configure the basic network settings,

.. code-block:: bash

  $ cat .me4cli.conf
  [API]
  api_username = manage
  api_password = XXXXXXXXX
  api_disable_tls_verification = True

  $ me4cli -f .me4cli.conf.initial_setup set network --api-host 10.0.0.2 --controller-a-ip 10.45.242.9 --controller-b-ip 10.45.242.10 --gateway 10.45.255.1 --netmask 255.255.0.0
  [ERROR] Exception ConnectionError: HTTPSConnectionPool(host='localhost', port=9000): Read timed out.

  $ me4cli -f .me4cli.conf.initial_setup show system-info --api-host rds-ost-jb39.bmc.cluster
  System: Uninitialized Name
    Product Type:    ME4084
    Contact:         Uninitialized Contact
    Description:     Uninitialized Info
    Location:        Uninitialized Location

  Service Tags:
    Enclosure 0:     FC8LZ23

.. code-block:: bash

   $ me4cli -f .me4cli.conf.rds-ost-jb39 set system-info --name rds-ost-jb39 --info "RDS OST" --contact support@hpc.cam.ac.uk --location "RCS UIS"

   $ me4cli -f .me4cli.conf.rds-ost-jb39 set ntp --status enabled --ntp-server 10.45.255.49

   $ me4cli -f .me4cli.conf.rds-ost-jb39 set dns --name-servers 10.45.255.50 --search-domains mgt.cluster bmc.cluster

   $ me4cli -f .me4cli.conf.rds-ost-jb39 set email --domain hpc.cam.ac.uk --server ppsw.cam.ac.uk --recipients storage-alerts@hpc.cam.ac.uk --sender root --notification-level error

  $

.. code-block::

  $ me4cli -f .me4cli.conf.rds-ost-jb39 configure disk-layout me4084-linear-raid6
  [INFO] Creating disk group: dg1-rds-ost-jb39, Disks: 0.2,0.10,0.18,0.26,0.34,0.44,0.52,0.60,0.68,0.76
  [INFO] Creating disk group: dg2-rds-ost-jb39, Disks: 0.3,0.11,0.19,0.27,0.35,0.45,0.53,0.61,0.69,0.77
  [INFO] Creating disk group: dg3-rds-ost-jb39, Disks: 0.4,0.12,0.20,0.28,0.36,0.46,0.54,0.62,0.70,0.78
  [INFO] Creating disk group: dg4-rds-ost-jb39, Disks: 0.5,0.13,0.21,0.29,0.37,0.47,0.55,0.63,0.71,0.79
  [INFO] Creating disk group: dg5-rds-ost-jb39, Disks: 0.6,0.14,0.22,0.30,0.38,0.48,0.56,0.64,0.72,0.80
  [INFO] Creating disk group: dg6-rds-ost-jb39, Disks: 0.7,0.15,0.23,0.31,0.39,0.49,0.57,0.65,0.73,0.81
  [INFO] Creating disk group: dg7-rds-ost-jb39, Disks: 0.8,0.16,0.24,0.32,0.40,0.50,0.58,0.66,0.74,0.82
  [INFO] Creating disk group: dg8-rds-ost-jb39, Disks: 0.9,0.17,0.25,0.33,0.41,0.51,0.59,0.67,0.75,0.83
  [INFO] Creating volume: v1-rds-ost-jb39, of size 85.4TiB on disk group: dg1-rds-ost-jb39
  [INFO] Creating volume: v2-rds-ost-jb39, of size 85.4TiB on disk group: dg2-rds-ost-jb39
  [INFO] Creating volume: v3-rds-ost-jb39, of size 85.4TiB on disk group: dg3-rds-ost-jb39
  [INFO] Creating volume: v4-rds-ost-jb39, of size 85.4TiB on disk group: dg4-rds-ost-jb39
  [INFO] Creating volume: v5-rds-ost-jb39, of size 85.4TiB on disk group: dg5-rds-ost-jb39
  [INFO] Creating volume: v6-rds-ost-jb39, of size 85.4TiB on disk group: dg6-rds-ost-jb39
  [INFO] Creating volume: v7-rds-ost-jb39, of size 85.4TiB on disk group: dg7-rds-ost-jb39
  [INFO] Creating volume: v8-rds-ost-jb39, of size 85.4TiB on disk group: dg8-rds-ost-jb39

.. code-block::

  $ me4cli -f .me4cli.conf.rds-ost-jb52 delete host-configuration
  [INFO] Deleting all host groups present...
  [INFO] Deleting all initiator nicknames...

  $ me4cli -f .me4cli.conf.rds-ost-jb52 configure host rds-oss51 --port-wwpn 0x54cd98f0c83fbe00 0x54cd98f0c83ffe00
  [INFO] Setting initiator nickname: rds-oss51-P0 to 54cd98f0c83fbe00
  [INFO] Setting initiator nickname: rds-oss51-P1 to 54cd98f0c83ffe00
  [INFO] Creating host: rds-oss51...
  [INFO] Creating host group: hg-rds-ost-jb52...

  $ me4cli -f .me4cli.conf.rds-ost-jb52 configure host rds-oss52 --port-wwpn 0x54cd98f0c83ed500 0x54cd98f0c83faf00
  [INFO] Setting initiator nickname: rds-oss52-P0 to 54cd98f0c83ed500
  [INFO] Setting initiator nickname: rds-oss52-P1 to 54cd98f0c83faf00
  [INFO] Creating host: rds-oss52...
  [INFO] Adding rds-oss52 to host group: hg-rds-ost-jb52...


.. code-block:: bash

  $ me4cli -f .me4cli.conf.rds-ost-jb52 configure mapping --host-group hg-rds-ost-jb52


