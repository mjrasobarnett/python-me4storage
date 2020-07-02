import logging

from me4storage.models.basemodel import Model
import me4storage.common.formatters as formatters

logger = logging.getLogger(__name__)

class Redundancy(Model):
    ''' Class to represent the redundancy model from the ME4 API
    https://www.dell.com/support/manuals/uk/en/ukbsdt1/powervault-me4012/me4_series_cli_pub/redundancy
    '''
    _attrs = {
        'redundancy-mode': '',
        'redundancy-mode-numeric': '',
        'redundancy-status': '',
        'redundancy-status-numeric': '',
        'controller-a-status': '',
        'controller-a-status-numeric': '',
        'controller-a-serial-number': '',
        'controller-b-status': '',
        'controller-b-status-numeric': '',
        'controller-b-serial-number': '',
        'other-MC-status': '',
        'other-MC-status-numeric': '',
        }
