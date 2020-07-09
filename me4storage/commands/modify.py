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

from me4storage.api import show, modify

logger = logging.getLogger(__name__)

def system_info(args):

    session = Session(baseurl = args.api_baseurl,
                      port = args.api_port,
                      username = args.api_username,
                      password = args.api_password,
                      verify = False if args.api_disable_tls_verification else True)

    modify.system_info(session,
                       name=args.system_name,
                       info=args.system_info,
                       contact=args.system_contact,
                       location=args.system_location)

    rc = CheckResult.OK
    return rc.value



