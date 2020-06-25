#!/usr/bin/env python
# pylint: disable-msg=C0103

"""
nsca

"""

import logging
import socket
import subprocess
import shutil
from enum import Enum

logger = logging.getLogger(__name__)

class CheckResult(Enum):
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3

def send_result(check_name, check_result, check_message):
    logger.info('Sending NSCA check_result via send_nsca')
    send_nsca_path = shutil.which('send_nsca')
    if not send_nsca_path:
        logger.error('Cannot find send_nsca in path. Aborting...')
        return False

    hostname = socket.getfqdn()
    nsca_msg = '{0},{1},{2},{3}'.format(hostname,check_name,check_result.value,check_message)
    logger.debug("Sending NSCA result: {}".format(nsca_msg))

    command = [send_nsca_path,'-v','-d,']

    try:
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(input=nsca_msg.encode('utf-8'))
        rc = process.returncode
        if rc != 0:
            logger.error('send_nsca command failed: {}'.format(" ".join(command)))
            logger.error('Command exited with return code ({})'.format(rc))
            logger.error(stdout.decode("utf-8"))
            logger.error(stderr.decode("utf-8"))
            return False
        else:
            return True

    except Exception as err:
        logger.error("Unable to run process: '{}' " \
                     "Error({}): {}".format(" ".join(command), err.errno, err.strerror))
        return False
