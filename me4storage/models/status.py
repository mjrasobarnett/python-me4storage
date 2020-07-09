import logging
from datetime import datetime

from me4storage.models.basemodel import Model
import me4storage.common.formatters as formatters

logger = logging.getLogger(__name__)

class Status(Model):
    ''' Class to represent the status model from the ME4 API
        https://www.dell.com/support/manuals/uk/en/ukbsdt1/powervault-me4012/me4_series_cli_pub/status
    '''
    _attrs = {
        'response-type': '',
        'response-type-numeric': '',
        'response': '',
        'return-code': '',
        'component-id': '',
        'time-stamp': '',
        'time-stamp-numeric': 'epoch',
        }
