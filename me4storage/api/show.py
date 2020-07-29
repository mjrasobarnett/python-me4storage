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
from me4storage.models.volume import Volume
from me4storage.models.initiator import Initiator
from me4storage.models.host_group import HostGroup
from me4storage.models.volume_view import VolumeView, VolumeViewMapping
from me4storage.models.host_group_view import HostGroupView, HostViewMapping
from me4storage.models.user import User

logger = logging.getLogger(__name__)

def users(session, user=None):
    params = {}
    if user is not None:
        params[user] = None

    response_body = session.get_object('show/users',params)
    # iterate over list of results and instantiate model object for each entry
    results = []
    for _dict in response_body.get('users',[]):
        results.append(User(_dict))

    return results

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

def volumes(session, detail=None, pool=None, disk_groups=None, volume_type=None, volumes=None):
    params = {}
    if detail is not None:
        params['detail'] = None
    if pool is not None:
        params['pool'] = None
    if (disk_groups is not None) and isinstance(disk_groups, list):
        params['vdisk'] = ",".join(disk_groups)
    if volume_type is not None:
        params['type'] = volume_type
    if (volumes is not None) and isinstance(volumes, list):
        params[",".join(volumes)] = None

    response_body = session.get_object('show/volumes',params)
    # iterate over list of results and instantiate model object for each entry
    results = []
    for _dict in response_body.get('volumes',[]):
        results.append(Volume(_dict))

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

def initiators(session, hosts=None, initiators=None):
    params = {}
    if (hosts is not None) and isinstance(hosts, list):
        params['hosts'] = ",".join(hosts)
    if (initiators is not None) and isinstance(initiators, list):
        params[",".join(initiators)] = None

    response_body = session.get_object('show/initiators',params)
    # iterate over list of results and instantiate model object for each entry
    results = []
    for _dict in response_body.get('initiator',[]):
        results.append(Initiator(_dict))

    return results

def host_groups(session, hosts=None, initiators=None):
    params = {}
    if (hosts is not None) and isinstance(hosts, list):
        params['hosts'] = ",".join(hosts)
    if (initiators is not None) and isinstance(initiators, list):
        params['initiators'] = ",".join(initiators)

    response_body = session.get_object('show/host-groups',params)
    # iterate over list of results and instantiate model object for each entry
    results = []
    for _dict in response_body.get('host-group',[]):
        results.append(HostGroup(_dict))

    return results

def mappings(session, show_all=None, show_initiator_mappings=None, initiators=None):
    params = {}
    if show_all is not None:
        params['all'] = None
    if show_initiator_mappings is not None:
        params['initiator'] = None
    if (initiators is not None) and isinstance(initiators, list):
        params['initiators'] = ",".join(initiators)

    response_body = session.get_object('show/maps',params)
    # iterate over list of results and instantiate model object for each entry
    results = []

    # model type depends on whether option to show initiator mappings was chosen
    if show_initiator_mappings is not None:
        for _dict in response_body.get('host-group-view',[]):
            results.append(HostGroupView(_dict))
    else:
        for _dict in response_body.get('volume-view',[]):
            results.append(VolumeView(_dict))

    return results

def volume_mappings(session, show_all=None, initiators=None):
    return mappings(session, show_all=show_all, initiators=initiators)

def host_group_mappings(session, show_all=None, initiators=None):
    return mappings(session, show_all=show_all, show_initiator_mappings=True, initiators=initiators)

def svc_tag(session):
    response_body = session.get_object('show/system')
    # iterate over list of results and instantiate model object for each entry
    results = []
    for _dict in response_body.get('system',[]):
        results.append(System(_dict))

    return results
