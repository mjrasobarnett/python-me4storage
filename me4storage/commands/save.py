import logging
import colorama
from colorama import Fore, Style
from terminaltables import SingleTable
from pprint import pformat
from datetime import datetime
import os
import pysftp
import shutil

from me4storage.api.session import Session
from me4storage.common.exceptions import ApiError
from me4storage.common.nsca import CheckResult
import me4storage.common.util as util
import me4storage.common.tables as tables
import me4storage.common.formatters

from me4storage.api import show
import me4storage.common.tables as tables

logger = logging.getLogger(__name__)
# Set paramiko logger to WARNING level because paramiko logging is quite noisy
# for our purposes, with many things (like authentication banner) logged to
# level INFO, which I prefer not to see
logging.getLogger("paramiko").setLevel(logging.WARNING)

def logs(args, session):

    if args.output_dir:
        output_dir = os.path.abspath(args.output_dir)
    else:
        output_dir = os.getcwd()

    if args.output_file:
        filename = args.output_file
    else:
        # Use default naming scheme
        systems = show.system(session)
        service_tags = show.service_tag_info(session)

        system_name = systems[0].system_name
        svc_tag = service_tags[0].service_tag
        date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        filename = f"logs_{system_name}_{svc_tag}_{date}.zip"

    output_file = os.path.join(output_dir, filename)

    cnopts = pysftp.CnOpts(knownhosts=os.path.expanduser(os.path.join('~','.ssh','known_hosts')))
    cnopts.hostkeys = None
    logger.info(f"Downloading log bundle from {args.api_host} to "
                f"{output_file} ... This can take a few minutes.")
    with pysftp.Connection(args.api_host,
                      port=int(args.sftp_port),
                      username=args.api_username,
                      password=args.api_password,
                      cnopts=cnopts,
                      ) as sftp:
        sftp.get(remotepath='/logs', localpath=output_file)

    rc = CheckResult.OK
    return rc.value
