import logging
import re
from datetime import datetime

from me4storage.models.basemodel import Model
import me4storage.common.formatters as formatters

logger = logging.getLogger(__name__)

class AdvancedSettingsTable(Model):
    ''' Class to represent the model from the ME4 API
    https://www.dell.com/support/manuals/en-uk/powervault-me4024/me4_series_cli_pub/advanced-settings-table?guid=guid-7975466f-1bb9-4a44-9332-1eecc92c0a01&lang=en-us
    '''
    _attrs = {
        'background-scrub': '',
        'background-scrub-numeric': '',
        'background-scrub-interval': '',
        'partner-firmware-upgrade': '',
        'partner-firmware-upgrade-numeric': '',
        'utility-priority': '',
        'utility-priority-numeric': '',
        'smart': '',
        'smart-numeric': '',
        'dynamic-spares': '',
        'emp-poll-rate': '',
        'host-cache-control': '',
        'host-cache-control-numeric': '',
        'sync-cache-mode': '',
        'sync-cache-mode-numeric': '',
        'independent-cache': '',
        'independent-cache-numeric': '',
        'missing-lun-response': '',
        'missing-lun-response-numeric': '',
        'controller-failure': '',
        'controller-failure-numeric': '',
        'super-cap-failure': '',
        'super-cap-failure-numeric': '',
        'compact-flash-failure': '',
        'compact-flash-failure-numeric': '',
        'power-supply-failure': '',
        'power-supply-failure-numeric': '',
        'fan-failure': '',
        'fan-failure-numeric': '',
        'temperature-exceeded': '',
        'temperature-exceeded-numeric': '',
        'partner-notify': '',
        'partner-notify-numeric': '',
        'auto-write-back': '',
        'auto-write-back-numeric': '',
        'disk-dsd-enable': '',
        'disk-dsd-enable-numeric': '',
        'disk-dsd-delay': '',
        'background-disk-scrub': '',
        'background-disk-scrub-numeric': '',
        'managed-logs': '',
        'managed-logs-numeric': '',
        'single-controller': '',
        'single-controller-numeric': '',
        'auto-stall-recovery': '',
        'auto-stall-recovery-numeric': '',
        'restart-on-capi-fail': '',
        'restart-on-capi-fail-numeric': '',
        'large-pools': '',
        'large-pools-numeric': '',
        'random-io-performance-optimization': '',
        'random-io-performance-optimization-numeric': '',
        'cache-flush-timeout': '',
        'cache-flush-timeout-numeric': '',
        }

