import logging
import re
from datetime import datetime

from me4storage.models.basemodel import Model
import me4storage.common.formatters as formatters

logger = logging.getLogger(__name__)

class Version(Model):
    ''' Class to represent the model from the ME4 API
    https://www.dell.com/support/manuals/uk/en/ukbsdt1/powervault-me4012/me4_series_cli_pub/versions?guid=guid-bd52f076-2a06-4f9f-905d-b7e60fc84af0&lang=en-us
    '''
    _attrs = {
        'object-name': '',
        'sc-cpu-type': '',
        'bundle-version': '',
        'bundle-base-version': '',
        'build-date': '',
        'sc-fw': '',
        'sc-baselevel': '',
        'sc-memory': '',
        'sc-fu-version': '',
        'sc-loader': '',
        'capi-version': '',
        'mc-fw': '',
        'mc-loader': '',
        'mc-base-fw': '',
        'fw-default-platform-brand': '',
        'fw-default-platform-brand-numeric': '',
        'ec-fw': '',
        'pld-rev': '',
        'prm-version': '',
        'hw-rev': '',
        'him-rev': '',
        'him-model': '',
        'backplane-type': '',
        'host-channel_revision': '',
        'disk-channel_revision': '',
        'mrc-version': '',
        'ctk-version': '',
        }
