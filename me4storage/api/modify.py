import logging
import os
import json
from pprint import pformat

from me4storage.common.exceptions import ApiError

logger = logging.getLogger(__name__)

def system_info(session,
           contact=None,
           info=None,
           location=None,
           name=None,
           ):

    data = {}
    if contact is not None:
        data['contact'] = contact
    if info is not None:
        data['info'] = info
    if location is not None:
        data['location'] = location
    if name is not None:
        data['name'] = name

    response = session.put('set/system',data)
    return response

