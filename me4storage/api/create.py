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
