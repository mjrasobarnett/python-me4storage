import logging
import re
from datetime import datetime

from me4storage.models.basemodel import Model
import me4storage.common.formatters as formatters

logger = logging.getLogger(__name__)

class NetworkParameters(Model):
    ''' Class to represent the network-parameters model from the ME4 API
    https://www.dell.com/support/manuals/uk/en/powervault-me4012/powervault-me4012/me4_series_cli_pub/network-parameters?guid=guid-4da6f278-c522-4b7b-900f-22be12d74e36&lang=en-us
    '''
    _attrs = {
        'durable-id': '',
        'active-version': '',
        'ip-address': '',
        'gateway': '',
        'subnet-mask': '',
        'mac-address': '',
        'addressing-mode': '',
        'addressing-mode-numeric': '',
        'link-speed': '',
        'link-speed-numeric': '',
        'duplex-mode': '',
        'duplex-mode-numeric': '',
        'health': '',
        'health-numeric': '',
        'health-reason': '',
        'health-recommendation': '',
        'ping-broadcast': '',
        'ping-broadcast-numeric': '',
        }

    @property
    def controller(self):
        try:
            controller = re.search('^mgmtport_(.+)$', self.durable_id).group(1)
        except AttributeError:
            controller = self.durable_id
        return controller.upper()



