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
from me4storage.models.disk_group import DiskGroup
from me4storage.models.pool import Pool
from me4storage.models.disk import Disk

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

def pools(session, pool_type=None, name=None):
    params = {}
    if pool_type is not None:
        params['type'] = pool_type
    if name is not None:
        params[name] = None

    response_body = session.get_object('show/pools',params)
    # iterate over list of results and instantiate model object for each entry
    results = []
    for _dict in response_body.get('pools',[]):
        results.append(Pool(_dict))

    return results

def disk_groups(session, detail=None, pool_name=None, disk_groups=None):
    params = {}
    if detail is not None:
        params['detail'] = None
    if pool_name is not None:
        params['pool'] = pool_name
    if (disk_groups is not None) and isinstance(disk_groups, list):
        params['disk-groups'] = ",".join(disk_groups)

    response_body = session.get_object('show/disk-groups',params)
    # iterate over list of results and instantiate model object for each entry
    results = []
    for _dict in response_body.get('disk-groups',[]):
        results.append(DiskGroup(_dict))

    return results

def disks(session, detail=None, disk_groups=None):
    params = {}
    if detail is not None:
        params['detail'] = None
    if (disk_groups is not None) and isinstance(disk_groups, list):
        params['disk-group'] = ",".join(disk_groups)

    response_body = session.get_object('show/disks',params)
    # iterate over list of results and instantiate model object for each entry
    results = []
    for _dict in response_body.get('drives',[]):
        results.append(Disk(_dict))

    return results
