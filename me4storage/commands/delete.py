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

