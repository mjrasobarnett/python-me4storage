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

logger = logging.getLogger(__name__)

def health_status(args, session):

    response = show.system(session)
    logger.debug(response)

    rc = CheckResult.OK
    for system in response.get('system',[]):
        print(f"System: {system['system-name']}")
        print(f"\tHealth: {system['health']}")
        print(f"\tProduct Type: {system['product-id']}")

    return rc.value


