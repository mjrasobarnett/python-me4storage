import logging
import re
from datetime import datetime

from me4storage.models.basemodel import Model
import me4storage.common.formatters as formatters

logger = logging.getLogger(__name__)

class Volume(Model):
    ''' Class to represent the volumes model from the ME4 API
    https://www.dell.com/support/manuals/us/en/04/powervault-me4012/me4_series_cli_pub/volumes?guid=guid-f48614b5-c874-4cd1-aded-af981114bb51&lang=en-us
    '''
    _attrs = {
        'durable-id': '',
        'url': '',
        'virtual-disk-name': '',
        'storage-pool-name': '',
#        'storage-pools-url': '',
        'volume-name': '',
        'size': '',
        'size-numeric': '',
        'total-size': '',
        'total-size-numeric': '',
        'allocated-size': '',
        'allocated-size-numeric': '',
        'storage-type': '',
        'storage-type-numeric': '',
        'owner': '',
        'owner-numeric': '',
        'preferred-owner': '',
        'preferred-owner-numeric': '',
        'serial-number': '',
        'write-policy': '',
        'write-policy-numeric': '',
        'cache-optimization': '',
        'cache-optimization-numeric': '',
        'read-ahead-size': '',
        'read-ahead-size-numeric': '',
        'volume-type': '',
        'volume-type-numeric': '',
        'volume-class': '',
        'volume-class-numeric': '',
        'tier-affinity': '',
        'tier-affinity-numeric': '',
        'snapshot': '',
        'snapshot-retention-priority': '',
        'snapshot-retention-priority-numeric': '',
        'volume-qualifier': '',
        'raidtype': '',
        'raidtype-numeric': '',
        'cs-replication-role': '',
        'cs-copy-dest': '',
        'cs-copy-dest-numeric': '',
        'cs-copy-src': '',
        'cs-copy-src-numeric': '',
        'cs-primary': '',
        'cs-primary-numeric': '',
        'cs-secondary': '',
        'cs-secondary-numeric': '',
        'health': '',
        'health-numeric': '',
        'health-reason': '',
        'health-recommendation': '',
        'volume-group': '',
        'group-key': '',
        }
