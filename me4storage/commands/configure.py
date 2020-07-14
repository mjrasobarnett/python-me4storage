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

from me4storage.api import show, modify, create
from me4storage import commands

logger = logging.getLogger(__name__)

def disk_layout_me4084_linear_raid6(args, session):
    """ Fully configure empty ME4084 into typical disk configuration for Lustre OSTs

    This is a high-level function to fully configure an un-configured ME4084
    into a typical configuration for use as Lustre OSTs. This configuration
    involves creating 8x Linear 10-disk RAID6 disk-groups

    """

    systems = show.system(session)
    system_name = systems[0].system_name

    disk_groups = show.disk_groups(session)
    if len(disk_groups) > 0:
        logger.warn(f"There are {len(disk_groups)} disk-groups already present. No action taken...")
        rc = CheckResult.WARNING
        return rc.value

    # Many assumptions baked in here.
    #
    # We expect 84 disks present, of which 80 are HDDs to be used to create
    # linear disk groups. The other 4 are either global-spare drives, or are
    # unused SSDs.
    #
    # We expect the first two slots of each drawer to be the 4 spare drives
    # so usable disks for configuration are:
    # 0.2-0.41 and 0.44-0.83 (where drawers range: 0.0-0.41 and 0.42-0.83)
    #
    # There is no way to make these raid-groups tolerate a draw failure,
    # like with the MD platform, thus we worry less about the exact layout
    # of the disks within the drawers
    logger.info(f"Creating disk group: dg1-{system_name}")
    create.linear_disk_group(session,
                             name=f"dg1-{system_name}",
                             disks="0.2-11",
                             chunk_size="128",
                             raid_level="raid6")

    logger.info(f"Creating disk group: dg2-{system_name}")
    create.linear_disk_group(session,
                             name=f"dg2-{system_name}",
                             disks="0.12-21",
                             chunk_size="128",
                             raid_level="raid6")

    logger.info(f"Creating disk group: dg3-{system_name}")
    create.linear_disk_group(session,
                             name=f"dg3-{system_name}",
                             disks="0.22-31",
                             chunk_size="128",
                             raid_level="raid6")

    logger.info(f"Creating disk group: dg4-{system_name}")
    create.linear_disk_group(session,
                             name=f"dg4-{system_name}",
                             disks="0.32-41",
                             chunk_size="128",
                             raid_level="raid6")

    logger.info(f"Creating disk group: dg5-{system_name}")
    create.linear_disk_group(session,
                             name=f"dg5-{system_name}",
                             disks="0.44-53",
                             chunk_size="128",
                             raid_level="raid6")

    logger.info(f"Creating disk group: dg6-{system_name}")
    create.linear_disk_group(session,
                             name=f"dg6-{system_name}",
                             disks="0.54-63",
                             chunk_size="128",
                             raid_level="raid6")

    logger.info(f"Creating disk group: dg7-{system_name}")
    create.linear_disk_group(session,
                             name=f"dg7-{system_name}",
                             disks="0.64-73",
                             chunk_size="128",
                             raid_level="raid6")

    logger.info(f"Creating disk group: dg8-{system_name}")
    create.linear_disk_group(session,
                             name=f"dg8-{system_name}",
                             disks="0.74-83",
                             chunk_size="128",
                             raid_level="raid6")

    rc = CheckResult.OK
    return rc.value
