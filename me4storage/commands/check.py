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
import me4storage.formatters as formatters
import me4storage.common.formatters

from me4storage.api import show

logger = logging.getLogger(__name__)

def health_status(args, session):

    system = next(iter(show.system(session)))
    disks = show.disks(session)
    service_tags = show.service_tag_info(session)

    if system.health == 'OK':
        rc = CheckResult.OK
    elif system.health == 'Degraded':
        rc = CheckResult.CRITICAL
    else:
        rc = CheckResult.UNKNOWN

    print(formatters.format_health(system, service_tags, disks))
    return rc.value

def firmware_version(args, session):

    expected_version = args.firmware_version

    rc = CheckResult.OK
    system = next(iter(show.system(session)))
    versions = show.versions(session)

    print(f"{Fore.WHITE}{Style.BRIGHT}System: {system.system_name}{Style.RESET_ALL}")

    # List of columns to print, as a tuple of attribute name,
    # and column title
    row_labels = [('bundle_version','Bundle Version'),
                  ]

    columns = [
               ('controller-a-versions','Controller A'),
               ('controller-b-versions','Controller B'),
              ]

    # Extract titles for table header
    table_header = ['', 'Expected Version'] + [column[1] for column in columns]
    table_rows = []

    for attribute, label in row_labels:

        logger.debug(attribute)
        row = []
        row.append(label)
        row.append(expected_version)

        # Loop over the controllers listed in 'columns', where
        # we identify which controller the 'version' corresponds to
        # by checking if the version's 'object_name' property matches
        # what we've defined here in 'columns'
        for controller_name, _ in columns:
            logger.debug(controller_name)
            for version in versions:
                if version.object_name == controller_name:
                    try:
                        actual_version = getattr(version, attribute)

                    except AttributeError as err:
                        raise ApiError("No attribute '{}' in version "
                                       "definition:\n{}".format(
                                            attribute,
                                            pformat(version),
                                            ))

                    if actual_version == expected_version:
                        row.append(f"{Fore.GREEN}{Style.BRIGHT}{actual_version}{Style.RESET_ALL}")
                    else:
                        rc = CheckResult.CRITICAL
                        row.append(f"{Fore.RED}{Style.BRIGHT}{actual_version}{Style.RESET_ALL}")

        table_rows.append(row)

    # Print table
    tables.display_table(table_header, table_rows, style='bordered')

    return rc.value


