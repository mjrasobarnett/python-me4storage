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

from me4storage.api import show
import me4storage.common.tables as tables

logger = logging.getLogger(__name__)

def system_info(args, session):

    systems = show.system(session)
    service_tags = show.service_tag_info(session)
    ntp_instances = show.ntp_status(session)

    rc = CheckResult.OK
    for system in systems:
        print(f"{Fore.WHITE}{Style.BRIGHT}System: {system.system_name}{Style.RESET_ALL}")
        print(f"  Product Type:    {system.product_id}")
        print(f"  Contact:         {system.system_contact}")
        print(f"  Description:     {system.system_information}")
        print(f"  Location:        {system.system_location}")

    print(f"\nService Tags:")
    for service_tag in service_tags:
        print(f"  Enclosure {service_tag.enclosure_id}:     {service_tag.service_tag}")

    return rc.value



def network(args, session):

    systems = show.system(session)
    network_parameters = show.network_parameters(session)
    ntp_instances = show.ntp_status(session)
    dns_instances = show.dns(session)
    hostnames = show.dns_management_hostname(session)

    rc = CheckResult.OK
    for system in systems:
        print(f"{Fore.WHITE}{Style.BRIGHT}System: {system.system_name}{Style.RESET_ALL}")

        print(f"\nIPv4:")
        for network in network_parameters:
            print(f"  Controller:        {network.controller}")
            print(f"    IP:              {network.ip_address}")
            print(f"    Subnet Mask:     {network.subnet_mask}")
            print(f"    Gateway:         {network.gateway}")
            print(f"    MAC:             {network.mac_address}")
            print(f"    DHCP Mode:       {network.addressing_mode}")
            print(f"    Health:          {network.health}")
            print("")

        print(f"NTP:")
        for ntp in ntp_instances:
            print(f"  Status:          {ntp.ntp_status}")
            print(f"  Server:          {ntp.ntp_server_address}")
            print(f"  Time (UTC):      {ntp.ntp_contact_time}")
            print("")

        print(f"DNS:")
        for dns in dns_instances:
            print(f"  Controller:        {dns.controller}")
            for mgmt in hostnames:
                if dns.controller_numeric == mgmt.controller_numeric:
                    print(f"    Mgmt Hostname:   {mgmt.mgmt_hostname}")
            print(f"    Server(s):       {dns.name_servers}")
            print(f"    Search Domains:  {dns.search_domains}")
            print("")

    return rc.value

def notifications(args, session):

    systems = show.system(session)
    email_params = show.email_parameters(session)

    rc = CheckResult.OK
    for system in systems:
        print(f"{Fore.WHITE}{Style.BRIGHT}System: {system.system_name}{Style.RESET_ALL}")

        print(f"\nEmail:")
        for email in email_params:
            print(f"  Status:        {email.email_notification}")
            print(f"  Level:         {email.email_notification_filter}")
            print(f"  Recipients:    {email.recipients}")
            print(f"  SMTP Server:   {email.email_server}:{email.email_smtp_port}")
            print(f"  Sender:        {email.email_sender}@{email.email_domain}")
            print("")

    return rc.value

def storage(args, session):

    systems = show.system(session)
    disk_groups = show.disk_groups(session, detail=True)

    for system in systems:
        print(f"{Fore.WHITE}{Style.BRIGHT}System: {system.system_name}{Style.RESET_ALL}")

    if args.detailed:
        # Print disks for each pool
        for dg in disk_groups:

            print(f"\n{Fore.WHITE}{Style.BRIGHT}Disk Group: {dg.name}{Style.RESET_ALL}")
            print(f"  Health:        {dg.health}")
            print(f"  Size:          {dg.size}")
            print(f"  Storage Type:  {dg.storage_type}")
            print(f"  Raid Level:    {dg.raidtype}")

            #######################################
            # PRINT Table of Volumes
            print(f"\n{Fore.WHITE}{Style.BRIGHT}Volumes:{Style.RESET_ALL}")
            volumes = show.volumes(session, disk_groups=[dg.name])
            # List of columns to print, as a tuple of attribute name,
            # and column title
            columns = [('volume_name','Name'),
                       ('virtual_disk_name','Disk Group'),
                       ('health','Health'),
                       ('size','Size'),
                       ('storage_type','Type'),
                       ('owner','Owner'),
                       ('preferred_owner','Pref. Owner'),
                       ('read_ahead_size','Read Ahead'),
                       ('write_policy','Write Policy'),
                       ]
            # Extract titles for table header
            table_header = [x[1] for x in columns]
            table_rows = []
            for volume in volumes:
                row = []
                for attribute, title in columns:
                    try:
                        row.append(getattr(volume,attribute))
                    except AttributeError as err:
                        raise ApiError("No attribute '{}' in volume "
                                       "definition:\n{}".format(
                                            attribute,
                                            pformat(volume),
                                            ))

                table_rows.append(row)

            # Print table
            tables.display_table(table_header, table_rows, style='bordered')

            #######################################
            # PRINT Table of DISKs
            print(f"\n{Fore.WHITE}{Style.BRIGHT}Disks:{Style.RESET_ALL}")
            disks = show.disks(session, disk_groups=[dg.name])

            # List of columns to print, as a tuple of attribute name,
            # and column title
            columns = [('location','Location'),
                       ('serial_number','Serial'),
                       ('vendor','Vendor'),
                       ('revision','Rev'),
                       ('interface','Interface'),
                       ('size','Size'),
                       ('status','Status'),
                       ('health','Health'),
                       ('architecture','Type'),
                       ('owner','Owner'),
                       ]
            # Extract titles for table header
            table_header = [x[1] for x in columns]
            table_rows = []
            for disk in disks:
                row = []
                for attribute, title in columns:
                    try:
                        row.append(getattr(disk,attribute))
                    except AttributeError as err:
                        raise ApiError("No attribute '{}' in disk "
                                       "definition:\n{}".format(
                                            attribute,
                                            pformat(disk),
                                            ))

                table_rows.append(row)

            # Print table
            tables.display_table(table_header, table_rows, style='bordered')

    else:
        # List of columns to print, as a tuple of attribute name,
        # and column title
        columns = [('name','Name'),
                   ('health','Health'),
                   ('size','Size'),
                   ('storage_type','Type'),
                   ('raidtype','Raid Level'),
                   ]

        # Extract titles for table header
        table_header = [x[1] for x in columns]
        table_rows = []

        for dg in disk_groups:
            row = []
            for attribute, title in columns:
                try:
                    row.append(getattr(dg,attribute))
                except AttributeError as err:
                    raise ApiError("No attribute '{}' in disk-group "
                                   "definition:\n{}".format(
                                        attribute,
                                        pformat(dg),
                                        ))

            table_rows.append(row)

        # Print table
        tables.display_table(table_header, table_rows, style='bordered')

    rc = CheckResult.OK
    return rc.value


def hosts(args, session):

    systems = show.system(session)

    host_groups = show.host_groups(session)
    initiators = show.initiators(session)

    for system in systems:
        print(f"{Fore.WHITE}{Style.BRIGHT}System: {system.system_name}{Style.RESET_ALL}")

    for host_group in host_groups:
        print(f"\n{Fore.WHITE}{Style.BRIGHT}Host Group: {host_group.name}{Style.RESET_ALL}")

        hosts = host_group.hosts
        # List of columns to print, as a tuple of attribute name,
        # and column title
        columns = [('durable_id','ID'),
                   ('name','Name'),
                   ('member_count','Initiators'),
                   ('serial_number','Serial'),
                   ]

        # Extract titles for table header
        table_header = [x[1] for x in columns]
        table_rows = []

        for host in hosts:
            row = []
            for attribute, title in columns:
                try:
                    row.append(getattr(host,attribute))
                except AttributeError as err:
                    raise ApiError("No attribute '{}' in host "
                                   "definition:\n{}".format(
                                        attribute,
                                        pformat(host),
                                        ))

            table_rows.append(row)

        # Print table
        tables.display_table(table_header, table_rows, style='bordered')


    print(f"\n{Fore.WHITE}{Style.BRIGHT}Initiators:{Style.RESET_ALL}")
    # List of columns to print, as a tuple of attribute name,
    # and column title
    columns = [('durable_id','id'),
               ('nickname','name'),
               ('host_bus_type','Type'),
               ('id','WWPN/IQN'),
               ('discovered','Discovered'),
               ('mapped','Mapped'),
               ('host_id','Host'),
               ('host_key','Host Key'),
               ]

    # Extract titles for table header
    table_header = [x[1] for x in columns]
    table_rows = []

    for initiator in initiators:
        row = []
        for attribute, title in columns:
            try:
                row.append(getattr(initiator,attribute))
            except AttributeError as err:
                raise ApiError("No attribute '{}' in initiator "
                               "definition:\n{}".format(
                                    attribute,
                                    pformat(initiator),
                                    ))

        table_rows.append(row)

    # Print table
    tables.display_table(table_header, table_rows, style='bordered')

    rc = CheckResult.OK
    return rc.value
