import logging
import os
import json
import re
from datetime import datetime
from colorama import Fore, Style
import textwrap

from me4storage.common.exceptions import ApiError
import me4storage.common.tables as tables
from pprint import pformat

logger = logging.getLogger(__name__)

def format_health(system, service_tags, detailed=False):
    output = []
    if system.health == 'OK':
        output.append(f"{Style.BRIGHT}Array Health: {Fore.GREEN}{Style.BRIGHT}{system.health}{Style.RESET_ALL}")
    elif system.health == 'Degraded':
        output.append(f"{Style.BRIGHT}Array Health: {Fore.RED}{Style.BRIGHT}{system.health}{Style.RESET_ALL}")
    else:
        output.append(f"{Style.BRIGHT}Array Health: {Fore.PURPLE}{Style.BRIGHT}{system.health}{Style.RESET_ALL}")

    health_output = "\n".join(output)
    system_output = format_system(system, service_tags)
    redundancy_output = format_system_redundancy(system)
    unhealthy_output = format_unhealthy_components(system)

    return health_output + "\n\n" \
           + system_output + "\n\n" \
           + redundancy_output + "\n\n" \
           + unhealthy_output

def format_certificates(system, certificates, detailed=False):
    output = []
    output.append(f"{Fore.WHITE}{Style.BRIGHT}System: {system.system_name}{Style.RESET_ALL}")
    output.append("")

    for certificate in certificates:
        output.append(f"{Fore.WHITE}{Style.BRIGHT}Controller: {certificate.controller} "
                      f"- {certificate.certificate_status}{Style.RESET_ALL}")
        output.append(f"Date added: {certificate.certificate_time}")
        output.append(f"Signature:  {certificate.certificate_signature}")
        if detailed:
            output.append("")
            output.append(re.sub(r'(\s{3,})', r'\n\1', certificate.certificate_text))

        output.append("")


    return "\n".join(output)

def format_system(system, service_tags):
    output = []

    output.append(f"{Fore.WHITE}{Style.BRIGHT}System: {system.system_name}{Style.RESET_ALL}")
    output.append(f"  Product Type:    {system.product_id}")
    output.append(f"  Contact:         {system.system_contact}")
    output.append(f"  Description:     {system.system_information}")
    output.append(f"  Location:        {system.system_location}")
    output.append("")

    output.append(f"{Style.BRIGHT}Service Tags:{Style.RESET_ALL}")
    for service_tag in service_tags:
        output.append(f"  Enclosure {service_tag.enclosure_id}:     {service_tag.service_tag}")


    return "\n".join(output)

def format_system_redundancy(system):
    output = []

    redundancy = next(iter(system.redundancy))
    output.append(f"{Fore.WHITE}{Style.BRIGHT}System Redundancy:{Style.RESET_ALL}")
    output.append(f"  Mode:            {redundancy.redundancy_mode}")

    if redundancy.redundancy_status == 'Redundant':
        output.append(f"  Status:          {Fore.GREEN}{Style.BRIGHT}{redundancy.redundancy_status}{Style.RESET_ALL}")
    else:
        output.append(f"  Status:          {Fore.RED}{Style.BRIGHT}{redundancy.redundancy_status}{Style.RESET_ALL}")

    controller_a_status = redundancy.controller_a_status
    controller_b_status = redundancy.controller_b_status
    secondary_mc_status = redundancy.other_mc_status

    if controller_a_status == 'Operational':
        output.append(f"  Controller A:    {Fore.GREEN}{Style.BRIGHT}{controller_a_status}{Style.RESET_ALL}")
    else:
        output.append(f"  Controller A:    {Fore.RED}{Style.BRIGHT}{controller_a_status}{Style.RESET_ALL}")

    if controller_b_status == 'Operational':
        output.append(f"  Controller B:    {Fore.GREEN}{Style.BRIGHT}{controller_b_status}{Style.RESET_ALL}")
    else:
        output.append(f"  Controller B:    {Fore.RED}{Style.BRIGHT}{controller_b_status}{Style.RESET_ALL}")

    if secondary_mc_status == 'Operational':
        output.append(f"  Secondary MC:    {Fore.GREEN}{Style.BRIGHT}{secondary_mc_status}{Style.RESET_ALL}")
    else:
        output.append(f"  Secondary MC:    {Fore.RED}{Style.BRIGHT}{secondary_mc_status}{Style.RESET_ALL}")
    output.append("")

    return "\n".join(output)

def format_unhealthy_components(system):
    output = []

    unhealthy_components = system.unhealthy_component

    if unhealthy_components:
        output.append(f"{Fore.WHITE}{Style.BRIGHT}Unhealthy Components:{Style.RESET_ALL}\n")
        prefix = "  "

    for component in unhealthy_components:
        output.append(f"{prefix}{Fore.WHITE}{Style.BRIGHT}Component Type:  {component.component_id}{Style.RESET_ALL}")
        output.append(f"{prefix}  ID:              {component.primary_key}")
        output.append(f"{prefix}  Component Type:  {component.basetype} - {component.component_type}")
        output.append(f"{prefix}  Health:          {Fore.RED}{Style.BRIGHT}{component.health}{Style.RESET_ALL}")
        health_reason = textwrap.indent(textwrap.dedent(textwrap.fill(component.health_reason)), f'{prefix}                   ')
        health_recommendation = textwrap.indent(textwrap.dedent(textwrap.fill(component.health_recommendation)), f'{prefix}                   ')
        output.append(f"{prefix}  Health Reason:\n   {health_reason}")
        output.append(f"{prefix}  Recommendation:\n  {health_recommendation}")
        output.append("")

    return "\n".join(output)

def format_advanced_settings(advanced_settings):

    # List of columns to print, as a tuple of attribute name,
    # and column title
    row_labels = [('background_scrub','Background Scrub (checks disks in disk groups)'),
                  ('background_scrub_interval','Background Scrub Interval'),
                  ('partner_firmware_upgrade','Partner Firmware Upgrade'),
                  ('utility_priority','Utility Priority'),
                  ('smart','SMART'),
                  ('dynamic_spares','Dynamic Spares'),
                  ('background_disk_scrub','Background Disk Scrub (checks disks not in disk groups)'),
                  ]

    columns = ['Setting',
               'Value',]

    # Extract titles for table header
    table_header = columns
    table_rows = []

    for attribute, label in row_labels:

        logger.debug(attribute)
        row = []
        row.append(label)

        try:
            row.append(getattr(advanced_settings, attribute))
        except AttributeError as err:
            raise ApiError("No attribute '{}' in version "
                           "definition:\n{}".format(
                                attribute,
                                pformat(advanced_settings),
                                ))

        table_rows.append(row)

    # Print table
    table = tables.format_table(table_header, table_rows, style='bordered')

    return table
