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

def system_info(args):

    session = Session(baseurl = args.api_baseurl,
                      port = args.api_port,
                      username = args.api_username,
                      password = args.api_password,
                      verify = False if args.api_disable_tls_verification else True)

    systems = show.system(session)
    service_tags = show.service_tag_info(session)

    rc = CheckResult.OK
    for system in systems:
        print(f"System: {system.system_name}")
        print(f"\tProduct Type: {system.product_id}")

    print(f"\nService Tags:")
    for service_tag in service_tags:
        print(f"\tEnclosure: {service_tag.enclosure_id} - {service_tag.service_tag}")

    return rc.value



