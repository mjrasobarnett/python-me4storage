import logging
import re
from datetime import datetime

from me4storage.models.basemodel import Model
import me4storage.common.formatters as formatters

logger = logging.getLogger(__name__)

class HostGroupView(Model):
    ''' Class to represent the host-group-view model from the ME4 API
    https://www.dell.com/support/manuals/uk/en/ukbsdt1/powervault-me4012/me4_series_cli_pub/host-group-view?guid=guid-3b2bd750-4f00-4fd2-9ed2-2e7c4ba07cd0&lang=en-us
    '''
    _attrs = {
        'durable-id': '',
        'serial-number': '',
        'group-name': '',
        }

    def _update_attributes(self, json_dict):
        """ Construct object from API response dict."""

        mapping_dicts = json_dict.pop('host-view-mappings', [])
        mapping_list = []
        for _dict in mapping_dicts:
            mapping_list.append(HostViewMapping(_dict))
        setattr(self, 'host_view_mappings', mapping_list)

        # Call base-class' _update_attributes method to extract
        # the remaining attributes
        super()._update_attributes(json_dict)



class HostViewMapping(Model):
    ''' Class to represent the host-view-mapping model from the ME4 API
    https://www.dell.com/support/manuals/uk/en/ukbsdt1/powervault-me4012/me4_series_cli_pub/host-view-mappings?guid=guid-904ff532-60ff-4053-b7be-c4269d351066&lang=en-us
    '''
    _attrs = {
        'volume': '',
        'volume-serial': '',
        'lun': '',
        'access': '',
        'access-numeric': '',
        'ports': '',
        }
