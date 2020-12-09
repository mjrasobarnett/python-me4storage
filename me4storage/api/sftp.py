import logging
import os
import json
from pprint import pformat
import pysftp

from me4storage.common.exceptions import ApiError

logger = logging.getLogger(__name__)

def save_logs(host, port, username, password, output_file):

    cnopts = pysftp.CnOpts(knownhosts=os.path.expanduser(os.path.join('~','.ssh','known_hosts')))
    cnopts.hostkeys = None
    logger.info(f"Downloading log bundle from {host} to "
                f"{output_file} ... This can take a few minutes.")
    with pysftp.Connection(host,
                      port=int(port),
                      username=username,
                      password=password,
                      cnopts=cnopts,
                      ) as sftp:
        sftp.get(remotepath='/logs', localpath=output_file)

    return True
