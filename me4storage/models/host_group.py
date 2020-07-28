import logging
import re
from datetime import datetime

from me4storage.models.basemodel import Model
import me4storage.common.formatters as formatters

logger = logging.getLogger(__name__)

class HostGroup(Model):
    ''' Class to represent the host-group model from the ME4 API
    https://www.dell.com/support/manuals/us/en/powervault-me4012/powervault-me4012/me4_series_cli_pub/show-host-groups?guid=guid-610896f7-daf1-449c-8ef9-c5eaf1140277&lang=en-us
    '''
    _attrs = {
        'durable-id': '',
        'name': '',
        'serial-number': '',
        'member-count': '',
        }

    def _update_attributes(self, json_dict):
        """ Construct object from API response dict."""

        host_dicts = json_dict.pop('hosts', [])
        host_list = []
        for _dict in host_dicts:
            host_list.append(Host(_dict))
        setattr(self, 'hosts', host_list)

        # Call base-class' _update_attributes method to extract
        # the remaining attributes
        super()._update_attributes(json_dict)
