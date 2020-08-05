import logging
from datetime import datetime

from me4storage.models.basemodel import Model
import me4storage.common.formatters as formatters

logger = logging.getLogger(__name__)

class CodeLoadReadiness(Model):
    ''' Class to represent the code-load-readiness model from the ME4 API
    https://www.dell.com/support/manuals/uk/en/ukbsdt1/powervault-me4012/me4_series_cli_pub/code-load-readiness?guid=guid-e34f2b4d-80b5-427d-8e43-92fe42c6d7c6&lang=en-us
    '''
    _attrs = {
        'overall-health': '',
        'overall-health-numeric': '',
        }

    def _update_attributes(self, json_dict):
        """ Construct object from API response dict."""

        reasons_dicts = json_dict.pop('code-load-readiness-reasons', [])
        reasons_list = []
        for _dict in reasons_dicts:
            reasons_list.append(CodeLoadReadinessReasons(_dict))
        setattr(self, 'code_load_readiness_reasons', reasons_list)

        # Call base-class' _update_attributes method to extract
        # the remaining attributes
        super()._update_attributes(json_dict)


class CodeLoadReadinessReasons(Model):
    ''' Class to represent the code-load-readiness model from the ME4 API
    https://www.dell.com/support/manuals/uk/en/ukbsdt1/powervault-me4012/me4_series_cli_pub/code-load-readiness-reasons?guid=guid-e105dc73-9e63-4614-898f-8b5c8605e542&lang=en-us
    '''
    _attrs = {
        'readiness-reason': '',
        'failure-risks': '',
        'failure-risks-numeric': '',
        }

