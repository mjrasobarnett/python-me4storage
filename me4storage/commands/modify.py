import logging
import colorama
from colorama import Fore, Style
from terminaltables import SingleTable
from pprint import pformat
import datetime

from me4storage.api.session import Session
from me4storage.common.exceptions import ApiError
from me4storage.common.nsca import CheckResult
import me4storage.common.util as util
import me4storage.common.tables as tables
import me4storage.common.formatters

from me4storage.api import show, modify
from me4storage import commands

logger = logging.getLogger(__name__)

def system_info(args, session):

    modify.system_info(session,
                       name=args.system_name,
                       info=args.system_info,
                       contact=args.system_contact,
                       location=args.system_location)

    controller_a_name = args.system_name + '-c0'
    controller_b_name = args.system_name + '-c1'

    modify.dns_management_hostname(session,
                                   controller='a',
                                   name=controller_a_name)
    modify.dns_management_hostname(session,
                                   controller='b',
                                   name=controller_b_name)

    commands.show.system_info(args, session)

    rc = CheckResult.OK
    return rc.value


def ntp(args, session):

    modify.ntp(session,
               status=args.status,
               ntp_server=args.ntp_server,
               timezone=args.timezone,)

    commands.show.network(args, session)

    rc = CheckResult.OK
    return rc.value

def dns(args, session):

    modify.dns(session,
               controller='both',
               name_servers=args.name_servers,
               search_domains=args.search_domains,)

    commands.show.network(args, session)

    rc = CheckResult.OK
    return rc.value

def network(args, session):

    modify.network(session,
                   controller='a',
                   ip=args.controller_a_ip,
                   gateway=args.gateway,
                   netmask=args.netmask,
                   )

    modify.network(session,
                   controller='b',
                   ip=args.controller_b_ip,
                   gateway=args.gateway,
                   netmask=args.netmask,
                   )

    logger.warning("May take up to 2 minutes for updated network settings to dislay...")
    commands.show.network(args, session)

    rc = CheckResult.OK
    return rc.value

def support_assist(args, session):

    modify.support_assist(session,
                   status=args.status
                   )

    rc = CheckResult.OK
    return rc.value

def email(args, session):

    modify.email(session,
                 domain=args.domain,
                 recipients=args.recipients,
                 security_protocol=args.security_protocol,
                 notification_level=args.notification_level,
                 port=args.port,
                 server=args.server,
                 sender=args.sender,
                )
    commands.show.notifications(args, session)

    rc = CheckResult.OK
    return rc.value
