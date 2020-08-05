import logging
from datetime import datetime

from me4storage.models.basemodel import Model
import me4storage.common.formatters as formatters

logger = logging.getLogger(__name__)

class User(Model):
    ''' Class to represent the users model from the ME4 API
    https://www.dell.com/support/manuals/uk/en/ukbsdt1/powervault-me4012/me4_series_cli_pub/users?guid=guid-35932210-b395-4f2b-b255-b7901485df10&lang=en-us
    '''
    _attrs = {
        'username': '',
        'roles': '',
        'user-type': '',
        'user-type-numeric': '',
        'user-locale': '',
        'user-locale-numeric': '',
        'interface-access-WBI': '',
        'interface-access-CLI': '',
        'interface-access-FTP': '',
        'interface-access-SMIS': '',
        'interface-access-SNMP': '',
        'storage-size-base': '',
        'storage-size-precision': '',
        'storage-size-units': '',
        'temperature-scale': '',
        'timeout': '',
        'authentication-type': '',
        'privacy-type': '',
        'password': '',
        'default-password-changed': '',
        'default-password-changed-numeric': '',
        'privacy-password': '',
        'trap-destination': '',
        }

    @property
    def ftp_enabled(self):
        if self.interface_access_ftp == 'x':
            return True
        else:
            return False

    @property
    def web_enabled(self):
        if self.interface_access_wbi == 'x':
            return True
        else:
            return False

    @property
    def cli_enabled(self):
        if self.interface_access_cli == 'x':
            return True
        else:
            return False
