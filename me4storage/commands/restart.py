import logging

from me4storage.api.session import Session
from me4storage.common.exceptions import ApiError
from me4storage.common.nsca import CheckResult
import me4storage.common.formatters
import me4storage.formatters as formatters

from me4storage.api import restart

logger = logging.getLogger(__name__)

def management_controllers(args, session):

    if args.controller:
        logger.info(f"Restarting management controllers {args.controller}...")
        controller = args.controller
    else:
        logger.info("Restarting both management controllers...")
        controller='both'

    restart.mc(session, controller=controller)

    return CheckResult.OK.value
