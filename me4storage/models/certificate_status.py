import logging
from datetime import datetime

from me4storage.models.basemodel import Model
import me4storage.common.formatters as formatters

logger = logging.getLogger(__name__)

class CertificateStatus(Model):
    ''' Class to represent the model from the ME4 API
    https://www.dell.com/support/manuals/uk/en/ukbsdt1/powervault-me4012/me4_series_cli_pub/certificate-status?guid=guid-45a2a58a-bee4-4e99-8949-f53c833f7418&lang=en-us
    '''
    _attrs = {
        'controller': '',
        'controller-numeric': '',
        'certificate-status': '',
        'certificate-status-numeric': '',
        'certificate-time': '',
        'certificate-signature': '',
        'certificate-text': '',
        }
