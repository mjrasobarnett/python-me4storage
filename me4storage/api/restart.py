import logging
import os
import json
from pprint import pformat

from me4storage.common.exceptions import ApiError

logger = logging.getLogger(__name__)

def mc(session, controller=None):
    params = {}
    if controller is not None:
        params[controller] = None

    response_body = session.get_object('restart/mc',params)
    return response_body

def sc(session, controller=None):
    params = {}
    if controller is not None:
        params[controller] = None

    response_body = session.get_object('restart/sc',params)
    return response_body
