import logging
import os
import json
from pprint import pformat

from me4storage.common.exceptions import ApiError

logger = logging.getLogger(__name__)

def pools(session,
          names,
          ):

    data = {}

    if isinstance(names, list):
        names_str = ",".join(names)
        data[names_str] = None

    response = session.put('delete/pools',data)
    return response

def host_groups(session,
                names,
                delete_hosts=None,
                ):

    data = {}

    if delete_hosts is not None:
        data['delete-hosts'] = None
    if isinstance(names, list):
        names_str = ",".join(names)
        data[names_str] = None

    response = session.put('delete/host-groups',data)
    return response

def initiator_nickname(session,
                       name,
                       ):

    data = {}
    data[name] = None
    response = session.put('delete/initiator-nickname',data)
    return response

def mapping(session,
         volumes,
         initiators,
         ):

    data = {}

    if isinstance(volumes, list):
        data[",".join(volumes)] = None
    if isinstance(initiators, list):
        data['initiator'] = ",".join(initiators)

    response = session.put('unmap/volume',data)
    return response
