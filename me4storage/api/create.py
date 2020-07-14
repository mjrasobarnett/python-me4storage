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

