import logging
import os
import json
from pprint import pformat

from me4storage.common.exceptions import ApiError

logger = logging.getLogger(__name__)

def linear_disk_group(session,
           name,
           disks,
           raid_level,
           assigned_controller='auto',
           chunk_size=None,
           spare_disks=None,
           ):

    data = {}

    data['type'] = 'linear'
    data[name] = None
    data['disks'] = disks
    data['assigned-to'] = assigned_controller
    data['level'] = raid_level

    if chunk_size is not None:
        data['chunk-size'] = chunk_size
    if spare_disks is not None:
        data['spare'] = spare_disks

    response = session.put('add/disk-group',data)
    return response

def virtual_disk_group(session,
           name,
           disks,
           raid_level,
           pool,
           ):

    data = {}

    data['type'] = 'virtual'
    data[name] = None
    data['disks'] = disks
    data['level'] = raid_level
    data['pool'] = pool

    response = session.put('add/disk-group',data)
    return response

def virtual_volume(session,
                  name,
                  pool,
                  size,
                  ):

    data = {}

    data[name] = None
    data['pool'] = pool
    data['size'] = size

    response = session.put('create/volume',data)
    return response

def linear_volume(session,
                  name,
                  disk_group,
                  size,
                  ):

    data = {}

    data[name] = None
    data['vdisk'] = disk_group
    data['size'] = size

    response = session.put('create/volume',data)
    return response

def host(session,
         name,
         host_group=None,
         initiators=None,
         ):

    data = {}

    data[name] = None
    if host_group is not None:
        data['host_group'] = host_group
    if (initiators is not None) and isinstance(initiators, list):
        data['initiators'] = ",".join(initiators)

    response = session.put('create/host',data)
    return response

def host_group(session,
         name,
         hosts,
         ):

    data = {}

    data[name] = None
    if isinstance(hosts, list):
        data['hosts'] = ",".join(hosts)

    response = session.put('create/host-group',data)
    return response

def mapping(session,
         volumes,
         initiators=None,
         lun=None,
         access=None,
         ):

    data = {}

    if isinstance(volumes, list):
        data[",".join(volumes)] = None
    if (initiators is not None) and isinstance(initiators, list):
        data['initiator'] = ",".join(initiators)
    if lun is not None:
        data['lun'] = lun
    if access is not None:
        data['access'] = access

    response = session.put('map/volume',data)
    return response

def user(session,
         name,
         password,
         base=None,
         interfaces=None,
         roles=None,
         timeout=None,
         ):

    data = {}

    data[name] = None
    data['password'] = password
    if base is not None:
        data['base'] = base
    if isinstance(interfaces, list):
        data['interfaces'] = ",".join(interfaces)
    if isinstance(roles, list):
        data['roles'] = ",".join(roles)
    if timeout is not None:
        data['timeout'] = timeout

    response = session.put('create/user',data)
    return response


