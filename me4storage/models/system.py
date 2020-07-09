import logging
from datetime import datetime

from me4storage.models.basemodel import Model
import me4storage.common.formatters as formatters

from me4storage.models.redundancy import Redundancy
from me4storage.models.unhealthy_component import UnhealthyComponent

logger = logging.getLogger(__name__)

class System(Model):
    ''' Class to represent the system model from the ME4 API
    https://www.dell.com/support/manuals/uk/en/ukbsdt1/powervault-me4012/me4_series_cli_pub/system
    '''
    _attrs = {
        'system-name': '',
        'system-contact': '',
        'system-location': '',
        'system-information': '',
        'midplane-serial-number': '',
        'vendor-name': '',
        'product-id': '',
        'product-brand': '',
        'scsi-vendor-id': '',
        'scsi-product-id': '',
        'enclosure-count': '',
        'health': '',
        'health-numeric': '',
        'health-reason': '',
        'other-MC-status': '',
        'other-MC-status-numeric': '',
        'pfuStatus': '',
        'supported-locales': '',
        'current-node-wwn': '',
        'fde-security-status': '',
        'fde-security-status-numeric': '',
        'platform-type': '',
        'platform-type-numeric': '',
        'platform-brand': '',
        'platform-brand-numeric': '',
        }

    def _update_attributes(self, json_dict):
        """ Construct object from API response dict."""


        redundancy_dicts = json_dict.pop('redundancy', [])
        redundancy_list = []
        for _dict in redundancy_dicts:
            redundancy_list.append(Redundancy(_dict))
        setattr(self, 'redundancy', redundancy_list)

        unhealthy_component_dicts = json_dict.pop('unhealthy-component', [])
        unhealthy_component_list = []
        for _dict in unhealthy_component_dicts:
            unhealthy_component_list.append(UnhealthyComponent(_dict))
        setattr(self, 'unhealthy_component', unhealthy_component_list)

        # Call base-class' _update_attributes method to extract
        # the remaining attributes
        super()._update_attributes(json_dict)

