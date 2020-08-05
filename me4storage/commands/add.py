import logging
import colorama
from colorama import Fore, Style
import datetime

from me4storage.api.session import Session
from me4storage.common.exceptions import ApiError
from me4storage.common.nsca import CheckResult
import me4storage.common.util as util
import me4storage.common.tables as tables
import me4storage.common.formatters

from me4storage.api import add, create

logger = logging.getLogger(__name__)

def user(args, session):

    name=args.username
    password=args.password
    base=args.base
    interfaces=args.interfaces
    roles=args.roles
    timeout=args.timeout

    create.user(session,
             name,
             password,
             base,
             interfaces,
             roles,
             timeout,
             )

    logger.info(f"Successfully added user: {name}")

    rc = CheckResult.OK
    return rc.value


