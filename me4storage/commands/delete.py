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

from me4storage.api import show, modify, delete
from me4storage import commands

logger = logging.getLogger(__name__)

def pool(args, session):

    pools = show.pools(session)
    pool_names = [pool.name for pool in pools]
    if len(pools) == 0:
        logger.warn(f"No pools present. Nothing to do...")
        rc = CheckResult.OK
        return rc.value

    if args.delete_pool_all is True:
        logger.info(f"Deleting all pools present...")
        delete.pools(session, pool_names)
    else:
        for requested_pool in args.delete_pool_names:
            if requested_pool not in pool_names:
                logger.warn(f"Pool {requested_pool} is not present. Nothing to do...")
                continue
            else:
                logger.info(f"Deleting pool {requested_pool}...")
                delete.pools(session, [requested_pool])

    rc = CheckResult.OK
    return rc.value

def host_group(args, session):

    host_groups = show.host_groups(session)
    host_group_names = [host_group.name for host_group in host_groups]
    if len(host_groups) == 0:
        logger.warn(f"No host_groups present. Nothing to do...")
        rc = CheckResult.OK
        return rc.value

    if args.delete_host_group_all is True:
        logger.info(f"Deleting all host groups present...")
        delete.host_groups(session,
                           names=['all'],
                           delete_hosts=args.delete_host_group_hosts)
    else:
        for requested_host_group in args.delete_host_group_names:
            if requested_host_group not in host_group_names:
                logger.warn(f"Host Group {requested_host_group} is not present. Nothing to do...")
                continue
            else:
                logger.info(f"Deleting host_group {requested_host_group}...")
                delete.host_groups(session,
                                   names=[requested_host_group],
                                   delete_hosts=args.delete_host_group_hosts)

    rc = CheckResult.OK
    return rc.value

def host_configuration(args, session):

    logger.info(f"Deleting all host groups present...")
    delete.host_groups(session,
                       names=['all'],
                       delete_hosts=True)

    logger.info(f"Deleting all initiator nicknames...")
    delete.initiator_nickname(session,
                              name='all')

    rc = CheckResult.OK
    return rc.value

def configuration(args, session):

    pools = show.pools(session)
    pool_names = [pool.name for pool in pools]
    if len(pools) > 0:
        logger.info(f"Deleting all pools present...")
        delete.pools(session, pool_names)
    else:
        logger.info(f"No pools present. Nothing to do...")

    logger.info(f"Deleting all host groups present...")
    delete.host_groups(session,
                       names=['all'],
                       delete_hosts=True)

    logger.info(f"Deleting all initiator nicknames...")
    delete.initiator_nickname(session,
                              name='all')

    rc = CheckResult.OK
    return rc.value

def mapping(args, session):
    # Check if host or host_group was requested to unmap from
    if args.delete_mapping_host_group:
        host_group = args.delete_mapping_host_group
        # Check if requested host group is configured
        host_groups = show.host_groups(session)
        if host_group not in [hg.name for hg in host_groups]:
            logger.error("Host group {host_group} not configured...")
            rc = CheckResult.CRITICAL
            return rc.value

        # Define initiators string, according to required syntax for mapping
        # See: https://www.dell.com/support/manuals/uk/en/ukbsdt1/powervault-me4012/me4_series_cli_pub/command-syntax?guid=guid-08ed6612-4713-4221-bc66-e3a6808b422a&lang=en-us
        initiators=f"{host_group}.*.*"
    else:
        host = args.delete_mapping_host
        # Define initiators string, according to required syntax for mapping
        # See: https://www.dell.com/support/manuals/uk/en/ukbsdt1/powervault-me4012/me4_series_cli_pub/command-syntax?guid=guid-08ed6612-4713-4221-bc66-e3a6808b422a&lang=en-us
        initiators=f"{host_group}.*"

    # Check if specific volume requested to unmap
    if args.delete_mapping_volume:
        volume_name = args.delete_mapping_volume.strip()
        volumes = show.volumes(session)
        if volume_name not in [vol.name for vol in volumes]:
            logger.error("Volume {volume_name} not present...")
            rc = CheckResult.CRITICAL
            return rc.value

        logger.info(f"Unmapping volume: {volume.volume_name} "
                    f"from initiators: {initiators}")
        delete.mapping(session,
                       initiators=[initiators],
                       volumes=[volume.volume_name])

    else:
        # Unmap all volumes from initiators
        volumes = show.volumes(session)
        for volume in volumes:
            logger.info(f"Unmapping volume: {volume.volume_name} "
                        f"from initiators: {initiators}")
            delete.mapping(session,
                           initiators=[initiators],
                           volumes=[volume.volume_name])

    rc = CheckResult.OK
    return rc.value
