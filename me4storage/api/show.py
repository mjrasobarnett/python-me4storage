import logging
import os
import json
from pprint import pformat

from me4storage.common.exceptions import ApiError
from me4storage.models.system import System
from me4storage.models.license import License
from me4storage.models.service_tag_info import ServiceTagInfo
from me4storage.models.ntp_status import NTPStatus
from me4storage.models.dns_parameters import DNSParameters
from me4storage.models.mgmt_hostnames import MGMTHostnames
from me4storage.models.network_parameters import NetworkParameters
from me4storage.models.email_parameters import EmailParameters

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

def ntp_status(session):
    response_body = session.get_object('show/ntp-status')
    # iterate over list of results and instantiate model object for each entry
    results = []
    for _dict in response_body.get('ntp-status',[]):
        results.append(NTPStatus(_dict))

    return results

def dns(session):
    response_body = session.get_object('show/dns-parameters')
    # iterate over list of results and instantiate model object for each entry
    results = []
    for _dict in response_body.get('dns-parameters',[]):
        results.append(DNSParameters(_dict))

    return results

def dns_management_hostname(session):
    response_body = session.get_object('show/dns-management-hostname')
    # iterate over list of results and instantiate model object for each entry
    results = []
    for _dict in response_body.get('mgmt-hostnames',[]):
        results.append(MGMTHostnames(_dict))

    return results

def network_parameters(session):
    response_body = session.get_object('show/network-parameters')
    # iterate over list of results and instantiate model object for each entry
    results = []
    for _dict in response_body.get('network-parameters',[]):
        results.append(NetworkParameters(_dict))

    return results

def email_parameters(session):
    response_body = session.get_object('show/email-parameters')
    # iterate over list of results and instantiate model object for each entry
    results = []
    for _dict in response_body.get('email-parameters',[]):
        results.append(EmailParameters(_dict))

    return results
