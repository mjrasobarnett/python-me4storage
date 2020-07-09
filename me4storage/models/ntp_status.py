import logging
from datetime import datetime

from me4storage.models.basemodel import Model
import me4storage.common.formatters as formatters

logger = logging.getLogger(__name__)

class NtpStatus(Model):
    ''' Class to represent the ntp-status model from the ME4 API
    https://www.dell.com/support/manuals/uk/en/powervault-me4012/powervault-me4012/me4_series_cli_pub/ntp-status?guid=guid-b95cb077-a24e-47f3-ac8e-885979649d23&lang=en-us
    '''
    _attrs = {
        'ntp-status': '',
        'ntp-server-address': '',
        'ntp-contact-time': '',
        }
