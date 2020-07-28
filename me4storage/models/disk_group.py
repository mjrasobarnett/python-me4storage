import logging
import re
from datetime import datetime

from me4storage.models.basemodel import Model
import me4storage.common.formatters as formatters

from me4storage.models.unhealthy_component import UnhealthyComponent

logger = logging.getLogger(__name__)

class DiskGroup(Model):
    ''' Class to represent the disk-groups model from the ME4 API
    https://www.dell.com/support/manuals/uk/en/ukbsdt1/powervault-me4012/me4_series_cli_pub/disk-groups?guid=guid-6bc8d9a9-12d1-4e4e-a047-45fc95694880&lang=en-us
    '''
    _attrs = {
        'name': '',
#        'url': '',
        'blocksize': '',
        'size': '',
        'size-numeric': '',
        'freespace': '',
        'freespace-numeric': '',
        'raw-size': '',
        'raw-size-numeric': '',
        'storage-type': '',
        'storage-type-numeric': '',
        'pool': '',
#        'pools-url': '',
        'pool-serial-number': '',
        'storage-tier': '',
        'storage-tier-numeric': '',
        'total-pages': '',
        'allocated-pages': '',
        'available-pages': '',
        'pool-percentage': '',
        'performance-rank': '',
        'owner': '',
        'owner-numeric': '',
        'preferred-owner': '',
        'preferred-owner-numeric': '',
        'raidtype': '',
        'raidtype-numeric': '',
        'diskcount': '',
        'sparecount': '',
        'chunksize': '',
        'status': '',
        'status-numeric': '',
        'lun': '',
        'min-drive-size': '',
        'min-drive-size-numeric': '',
        'create-date': '',
        'create-date-numeric': '',
        'cache-read-ahead': '',
        'cache-read-ahead-numeric': '',
        'cache-flush-period': '',
        'read-ahead-enabled': '',
        'read-ahead-enabled-numeric': '',
        'write-back-enabled': '',
        'write-back-enabled-numeric': '',
        'job-running': '',
        'current-job': '',
        'current-job-numeric': '',
        'current-job-completion': '',
        'num-array-partitions': '',
        'largest-free-partition-space': '',
        'largest-free-partition-space-numeric': '',
        'num-drives-per-low-level-array': '',
        'num-expansion-partitions': '',
        'num-partition-segments': '',
        'new-partition-lba': '',
        'new-partition-lba-numeric': '',
        'array-drive-type': '',
        'array-drive-type-numeric': '',
        'disk-description': '',
        'disk-description-numeric': '',
        'is-job-auto-abortable': '',
        'is-job-auto-abortable-numeric': '',
        'serial-number': '',
        'blocks': '',
#        'blocks-numeric': '',
        'disk-dsd-enable-vdisk': '',
        'disk-dsd-enable-vdisk-numeric': '',
        'disk-dsd-delay-vdisk': '',
        'adapt-target-spare-capacity': '',
        'adapt-target-spare-capacity-numeric': '',
        'adapt-actual-spare-capacity': '',
        'adapt-actual-spare-capacity-numeric': '',
        'adapt-critical-capacity': '',
        'adapt-critical-capacity-numeric': '',
        'adapt-degraded-capacity': '',
        'adapt-degraded-capacity-numeric': '',
        'adapt-linear-volume-boundary': '',
        'pool-sector-format': '',
        'pool-sector-format-numeric': '',
        'health': '',
        'health-numeric': '',
        'health-reason': '',
        'health-recommendation': '',
#        'unhealthy-component': '',
        }

    def _update_attributes(self, json_dict):
        """ Construct object from API response dict."""

        unhealthy_component_dicts = json_dict.pop('unhealthy-component', [])
        unhealthy_component_list = []
        for _dict in unhealthy_component_dicts:
            unhealthy_component_list.append(UnhealthyComponent(_dict))
        setattr(self, 'unhealthy_component', unhealthy_component_list)

        # Call base-class' _update_attributes method to extract
        # the remaining attributes
        super()._update_attributes(json_dict)



