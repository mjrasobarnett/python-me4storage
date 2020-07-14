import logging
import re
from datetime import datetime

from me4storage.models.basemodel import Model
import me4storage.common.formatters as formatters

from me4storage.models.unhealthy_component import UnhealthyComponent
from me4storage.models.disk_group import DiskGroup
from me4storage.models.tier import Tier

logger = logging.getLogger(__name__)

class Pool(Model):
    ''' Class to represent the pools model from the ME4 API
    https://www.dell.com/support/manuals/uk/en/ukbsdt1/powervault-me4012/me4_series_cli_pub/pools?guid=guid-59b21fc9-2cc9-4d8e-a2a0-561daae3cb3b&lang=en-us
    '''
    _attrs = {
        'name': '',
        'serial-number': '',
        'url': '',
        'storage-type': '',
        'storage-type-numeric': '',
        'blocksize': '',
        'total-size': '',
        'total-size-numeric': '',
        'total-avail': '',
        'total-avail-numeric': '',
        'snap-size': '',
        'snap-size-numeric': '',
        'allocated-pages': '',
        'available-pages': '',
        'overcommit': '',
        'overcommit-numeric': '',
        'over-committed': '',
        'over-committed-numeric': '',
        'volumes': '',
        'page-size': '',
        'page-size-numeric': '',
        'low-threshold': '',
        'middle-threshold': '',
        'high-threshold': '',
        'utility-running': '',
        'utility-running-numeric': '',
        'preferred-owner': '',
        'preferred-owner-numeric': '',
        'owner': '',
        'owner-numeric': '',
        'rebalance': '',
        'rebalance-numeric': '',
        'migration': '',
        'migration-numeric': '',
        'zero-scan': '',
        'zero-scan-numeric': '',
        'idle-page-check': '',
        'idle-page-check-numeric': '',
        'read-flash-cache': '',
        'read-flash-cache-numeric': '',
        'metadata-vol-size': '',
        'metadata-vol-size-numeric': '',
        'total-rfc-size': '',
        'total-rfc-size-numeric': '',
        'available-rfc-size': '',
        'available-rfc-size-numeric': '',
        'reserved-size': '',
        'reserved-size-numeric': '',
        'reserved-unalloc-size': '',
        'reserved-unalloc-size-numeric': '',
        'pool-sector-format': '',
        'pool-sector-format-numeric': '',
        'health': '',
        'health-numeric': '',
        'health-reason': '',
        'health-recommendation': '',
        }

    def _update_attributes(self, json_dict):
        """ Construct object from API response dict."""

        disk_group_dicts = json_dict.pop('disk-groups', [])
        disk_group_list = []
        for _dict in disk_group_dicts:
            disk_group_list.append(DiskGroup(_dict))
        setattr(self, 'disk_groups', disk_group_list)

        tier_dicts = json_dict.pop('tiers', [])
        tier_list = []
        for _dict in tier_dicts:
            tier_list.append(Tier(_dict))
        setattr(self, 'tiers', tier_list)

        unhealthy_component_dicts = json_dict.pop('unhealthy-component', [])
        unhealthy_component_list = []
        for _dict in unhealthy_component_dicts:
            unhealthy_component_list.append(UnhealthyComponent(_dict))
        setattr(self, 'unhealthy_component', unhealthy_component_list)

        # Call base-class' _update_attributes method to extract
        # the remaining attributes
        super()._update_attributes(json_dict)


