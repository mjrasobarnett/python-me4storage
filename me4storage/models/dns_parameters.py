import logging
from datetime import datetime

from me4storage.models.basemodel import Model
import me4storage.common.formatters as formatters

logger = logging.getLogger(__name__)

class DNSParameters(Model):
    ''' Class to represent the dns-parameters model from the ME4 API
    https://www.dell.com/support/manuals/uk/en/ukbsdt1/powervault-me4012/me4_series_cli_pub/controller-dns-parameters?guid=guid-fdad9529-ece5-4e4c-af6e-9421c01d5e72&lang=en-us
    '''
    _attrs = {
        'controller': '',
        'controller-numeric': '',
        'name-servers': '',
        'search-domains': '',
        }

