import logging
import os
import json
from pprint import pformat

from me4storage.common.exceptions import ApiError
from me4storage.models.code_load_readiness import CodeLoadReadiness, CodeLoadReadinessReasons

logger = logging.getLogger(__name__)

def firmware_upgrade_health(session):
    params = {}

    response_body = session.get_object('check/firmware-upgrade-health',params)
    # iterate over list of results and instantiate model object for each entry
    results = []
    for _dict in response_body.get('code-load-readiness',[]):
        results.append(CodeLoadReadiness(_dict))

    return results

