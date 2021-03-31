import os
import logging
import colorama
from colorama import Fore, Style
from terminaltables import SingleTable
from pprint import pformat
from datetime import datetime
import time
import tempfile

from me4storage.api.session import Session
import me4storage.api.sftp as sftp
from me4storage.common.exceptions import ApiError, UsageError
from me4storage.common.nsca import CheckResult
import me4storage.common.util as util
import me4storage.common.tables as tables
import me4storage.common.formatters
import me4storage.formatters as formatters

from me4storage.api import show

logger = logging.getLogger(__name__)

def logs(args, session):

    if (not args.email_sender) or (not args.email_recipient):
        raise UsageError("--sender and --recipient must be given")

    system = next(iter(show.system(session)))
    service_tags = show.service_tag_info(session)
    service_tag = next(iter(service_tags))

    # Save storage health output
    health_text = util.strip_ansi_escape(formatters.format_health(system, service_tags))


    # Compose standard filename for log bundle
    system_name = system.system_name
    svc_tag = service_tag.service_tag
    date = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
    filename = f"logs_{system_name}_{svc_tag}_{date}.zip"

    email_subject = f"{args.email_prefix}: {system_name} - {svc_tag}"

    email_body = f"""
CHASSIS NAME: {system_name}
ARRAY SVC TAG: {svc_tag}
DATE: {time.strftime("%Y-%m-%d %H:%M")}

Health Status:
{{noformat}}
{health_text}
{{noformat}}

"""

    # Generate temporary directory to store the log file before emailing it
    with tempfile.TemporaryDirectory() as tmpdirname:
        logfile = os.path.join(tmpdirname, filename)

        sftp.save_logs(args.api_host,
                       args.sftp_port,
                       args.api_username,
                       args.api_password,
                       logfile)

        util.send_email(args.email_sender,
                        args.email_recipient,
                        email_subject,
                        email_body,
                        attachments=[logfile])

    rc = CheckResult.OK
    return rc.value
