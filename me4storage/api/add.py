import logging
import os
import json
from pprint import pformat

from me4storage.common.exceptions import ApiError

logger = logging.getLogger(__name__)

def host_group_members(session,
         name,
         hosts,
         ):

    data = {}

    data[name] = None
    if isinstance(hosts, list):
        data['hosts'] = ",".join(hosts)

    response = session.put('add/host-group-members',data)
    return response

