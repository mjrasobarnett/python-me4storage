import logging
import re
from datetime import datetime

from me4storage.models.basemodel import Model
import me4storage.common.formatters as formatters

logger = logging.getLogger(__name__)

class Initiator(Model):
    ''' Class to represent the initiator model from the ME4 API
    https://www.dell.com/support/manuals/us/en/04/powervault-me4012/me4_series_cli_pub/initiator?guid=guid-cedb2c5c-bdc6-4e0b-85fb-669cda536a46&lang=en-us
    '''
    _attrs = {
        'durable-id': '',
        'nickname': '',
        'discovered': '',
        'mapped': '',
        'profile': '',
        'profile-numeric': '',
        'host-bus-type': '',
        'host-bus-type-numeric': '',
        'id': '',
        'host-id': '',
        'host-key': '',
        'host-port-bits-a': '',
        'host-port-bits-b': '',
        }
