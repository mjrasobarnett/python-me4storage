import logging

from me4storage.models.basemodel import Model
import me4storage.common.formatters as formatters

logger = logging.getLogger(__name__)

class ServiceTagInfo(Model):
    ''' Class to represent the service-tag-info model from the ME4 API
    https://www.dell.com/support/manuals/uk/en/ukbsdt1/powervault-me4012/me4_series_cli_pub/service-tag-info
    '''
    _attrs = {
        'service-tag': '',
        'enclosure-id': '',
        }


