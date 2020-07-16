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
