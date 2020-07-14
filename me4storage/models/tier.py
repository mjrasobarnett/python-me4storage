import logging
import re
from datetime import datetime

from me4storage.models.basemodel import Model
import me4storage.common.formatters as formatters

logger = logging.getLogger(__name__)

class Tier(Model):
    ''' Class to represent the tiers model from the ME4 API
    https://www.dell.com/support/manuals/uk/en/ukbsdt1/powervault-me4012/me4_series_cli_pub/tiers?guid=guid-b88fe4ee-9096-40e7-9d43-a633488f8835&lang=en-us
    '''
    _attrs = {
        'serial-number': '',
        'pool': '',
        'tier': '',
        'pool-percentage': '',
        'diskcount': '',
        'raw-size': '',
        'raw-size-numeric': '',
        'total-size': '',
        'total-size-numeric': '',
        'allocated-size': '',
        'allocated-size-numeric': '',
        'available-size': '',
        'available-size-numeric': '',
        'affinity-size': '',
        'affinity-size-numeric': '',
        }
