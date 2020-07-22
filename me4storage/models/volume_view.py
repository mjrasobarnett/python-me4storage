import logging
import re
from datetime import datetime

from me4storage.models.basemodel import Model
import me4storage.common.formatters as formatters

logger = logging.getLogger(__name__)

class VolumeView(Model):
    ''' Class to represent the volume-view model from the ME4 API
    https://www.dell.com/support/manuals/uk/en/ukbsdt1/powervault-me4012/me4_series_cli_pub/volume-view?guid=guid-a3031c70-52a3-4698-be75-959b2b6a4482&lang=en-us
    '''
    _attrs = {
        'durable-id': '',
        'volume-serial': '',
        'volume-name': '',
        }

    def _update_attributes(self, json_dict):
        """ Construct object from API response dict."""

        mapping_dicts = json_dict.pop('volume-view-mappings', [])
        mapping_list = []
        for _dict in mapping_dicts:
            mapping_list.append(VolumeViewMapping(_dict))
        setattr(self, 'volume_view_mappings', mapping_list)

        # Call base-class' _update_attributes method to extract
        # the remaining attributes
        super()._update_attributes(json_dict)



class VolumeViewMapping(Model):
    ''' Class to represent the volume-view-mapping model from the ME4 API
    https://www.dell.com/support/manuals/uk/en/ukbsdt1/powervault-me4012/me4_series_cli_pub/volume-view-mappings?guid=guid-7e629aee-0e74-43e4-9190-d0fddad08c56&lang=en-us
    '''
    _attrs = {
        'durable-id': '',
        'parent-id': '',
        'mapped-id': '',
        'ports': '',
        'lun': '',
        'access': '',
        'access-numeric': '',
        'identifier': '',
        'nickname': '',
        'host-profile': '',
        'host-profile-numeric': '',
        }
