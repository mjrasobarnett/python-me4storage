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


