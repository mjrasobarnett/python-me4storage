import logging
import os
import json
from pprint import pformat

from me4storage.common.exceptions import ApiError
from me4storage.models.system import System
from me4storage.models.license import License
from me4storage.models.service_tag_info import ServiceTagInfo

logger = logging.getLogger(__name__)

def system(session):
    response_body = session.get_object('show/system')
    # iterate over list of results and instantiate model object for each entry
    results = []
    for _dict in response_body.get('system',[]):
        results.append(System(_dict))

    return results

def license(session):
    response_body = session.get_object('show/license')
    # iterate over list of results and instantiate model object for each entry
    results = []
    for _dict in response_body.get('license',[]):
        results.append(License(_dict))

    return results

def service_tag_info(session):
    response_body = session.get_object('show/service-tag-info')
    # iterate over list of results and instantiate model object for each entry
    results = []
    for _dict in response_body.get('service-tag-info',[]):
        results.append(ServiceTagInfo(_dict))

    return results
