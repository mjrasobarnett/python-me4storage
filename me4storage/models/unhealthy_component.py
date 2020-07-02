import logging

from me4storage.models.basemodel import Model
import me4storage.common.formatters as formatters

logger = logging.getLogger(__name__)

class UnhealthyComponent(Model):
    ''' Class to represent the redundancy model from the ME4 API
    https://www.dell.com/support/manuals/uk/en/ukbsdt1/powervault-me4012/me4_series_cli_pub/unhealthy-component
    '''
    _attrs = {
        'component-type': '',
        'component-type-numeric': '',
        'component-id': '',
        'basetype': '',
        'primary-key': '',
        'health': '',
        'health-numeric': '',
        'health-reason': '',
        'health-recommendation': '',
        }

