import logging
from datetime import datetime

from me4storage.models.basemodel import Model
import me4storage.common.formatters as formatters

logger = logging.getLogger(__name__)

class MGMTHostnames(Model):
    ''' Class to represent the dns-parameters model from the ME4 API
    https://www.dell.com/support/manuals/uk/en/ukbsdt1/powervault-me4012/me4_series_cli_pub/mgmt-hostnames?guid=guid-16daaaf4-3f27-4608-be44-79644aaf2ef1&lang=en-us
    '''
    _attrs = {
        'controller': '',
        'controller-numeric': '',
        'mgmt-hostname': '',
        'domain-name': '',
        }

