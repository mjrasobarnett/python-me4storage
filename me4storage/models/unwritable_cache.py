import logging
from datetime import datetime

from me4storage.models.basemodel import Model
import me4storage.common.formatters as formatters

logger = logging.getLogger(__name__)

class UnwritableCache(Model):
    ''' Class to represent the model from the ME4 API
    https://www.dell.com/support/manuals/uk/en/ukbsdt1/powervault-me4012/me4_series_cli_pub/unwritable-cache?guid=guid-904f797c-6250-4db2-bede-1dcf0bddcd42&lang=en-us
    '''
    _attrs = {
        'unwritable-a-percentage': '',
        'unwritable-b-percentage': '',
        }

    @property
    def has_unwritable_data(self):
        if (self.unwritable_a_percentage > 0) or \
           (self.unwritable_b_percentage > 0):
            return True
        else:
            return False
