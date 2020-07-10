import logging
import os
import json
from pprint import pformat

from me4storage.common.exceptions import ApiError

logger = logging.getLogger(__name__)

def system_info(session,
           contact=None,
           info=None,
           location=None,
           name=None,
           ):

    data = {}
    if contact is not None:
        data['contact'] = contact
    if info is not None:
        data['info'] = info
    if location is not None:
        data['location'] = location
    if name is not None:
        data['name'] = name

    response = session.put('set/system',data)
    return response

def ntp(session,
        status=None,
        ntp_server=None,
        timezone=None,
        ):

    data = {}
    if status is not None:
        data['ntp'] = status
    if ntp_server is not None:
        data['ntpaddress'] = ntp_server
    if timezone is not None:
        data['timezone'] = timezone

    response = session.put('set/ntp-parameters',data)
    return response

def dns_management_hostname(session,
        controller=None,
        name=None,
        ):

    data = {}
    if controller is not None:
        data['controller'] = controller
    if name is not None:
        data['name'] = name

    response = session.put('set/dns-management-hostname',data)
    return response

def dns(session,
        controller=None,
        name_servers=None,
        search_domains=None,
        ):

    data = {}
    if controller is not None:
        data['controller'] = controller
    if (name_servers is not None) and isinstance(name_servers, list):
        data['nameservers'] = ",".join(name_servers)
    if (search_domains is not None) and isinstance(search_domains, list):
        data['search-domains'] = ",".join(search_domains)

    response = session.put('set/dns-parameters',data)
    return response

def network(session,
        controller=None,
        dhcp=None,
        ip=None,
        gateway=None,
        netmask=None,
        ):

    data = {}
    if controller is not None:
        data['controller'] = controller
    if dhcp is not None:
        # 'dhcp' doesn't take a value, provide None to omit this
        data['dhcp'] = None
    if ip is not None:
        data['ip'] = ip
    if gateway is not None:
        data['gateway'] = gateway
    if netmask is not None:
        data['netmask'] = netmask

    response = session.put('set/network-parameters',data)
    return response

def support_assist(session,
        status=None,
        ):

    data = {}
    if status is not None:
        # No parameter name here, the parameter is the value itself
        # 'enabled' or 'disabled'
        data[status] = None

    response = session.put('set/support-assist',data)
    return response

def email(session,
        domain=None,
        recipients=None,
        notification_level=None,
        security_protocol=None,
        port=None,
        server=None,
        sender=None,
        ):

    data = {}
    if domain is not None:
        data['domain'] = domain
    if (recipients is not None) and isinstance(recipients, list):
        data['email-list'] = ",".join(recipients)
    if security_protocol is not None:
        data['security-protocol'] = security_protocol
    if notification_level is not None:
        data['notification-level'] = notification_level
    if port is not None:
        data['port'] = port
    if server is not None:
        data['server'] = server
    if sender is not None:
        data['sender'] = sender

    response = session.put('set/email-parameters',data)
    return response
