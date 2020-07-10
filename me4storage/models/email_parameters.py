import logging
import re
from datetime import datetime

from me4storage.models.basemodel import Model
import me4storage.common.formatters as formatters

logger = logging.getLogger(__name__)

class EmailParameters(Model):
    ''' Class to represent the email-parameters model from the ME4 API
    https://www.dell.com/support/manuals/uk/en/ukbsdt1/powervault-me4012/me4_series_cli_pub/show-email-parameters?guid=guid-28f00cb2-fe8f-4062-a4dd-0b34f96d919e&lang=en-us
    '''
    _attrs = {
        'email-notification': '',
        'email-notification-numeric': '',
        'email-notification-filter': '',
        'email-notification-filter-numeric': '',
        'email-notify-address-1': '',
        'email-notify-address-2': '',
        'email-notify-address-3': '',
        'email-notify-address-4': '',
        'email-security-protocol': '',
        'email-security-protocol-numeric': '',
        'email-smtp-port': '',
        'email-server': '',
        'email-domain': '',
        'email-sender': '',
        'email-sender-password': '',
        'email-include-logs': '',
        'email-include-logs-numeric': '',
        }

    @property
    def recipients(self):
        return ",".join([self.email_notify_address_1,
                         self.email_notify_address_2,
                         self.email_notify_address_3,])
