import logging
import os
import json
from pprint import pformat

from me4storage.common.exceptions import ApiError

logger = logging.getLogger(__name__)

def system(session):
    response_body = session.get_object('show/system')
    return response_body

