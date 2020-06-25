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

logger = logging.getLogger(__name__)

def health_status(args):

    session = Session(baseurl = args.api_baseurl,
                      port = args.api_port,
                      version = args.api_version,
                      username = args.api_username,
                      password = args.api_password,
                      verify = False if args.api_disable_tls_verification else True)



