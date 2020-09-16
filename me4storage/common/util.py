# pylint: disable-msg=C0103

from __future__ import print_function
import argparse
import logging
import sys
import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

from colorama import Fore, Style

# Colour struct to hold console colour codes
class Colour(object):
  RED = '\033[1;31m'
  BLUE = "\033[1;34m"
  PURP = "\033[1;35m"
  TEAL = "\033[1;36m"
  ORANGE = "\033[0;33m"
  YEL = "\033[1;33m"
  GREEN = "\033[1;32m"
  WHITE = "\033[1;00m"
  GREY = "\033[1;37m"
  CLEAR = "\033[0m"

# fs-like log format with a thread name prefix
PREFIX = "%(asctime)s "
LEVEL = "[%(levelname)s] "
DATE_FORMAT = '%b %d %H:%M:%S'
VERBOSE_LOG_FORMAT = PREFIX + LEVEL + (
    "%(filename)s:%(lineno)d : %(message)s")
SHORT_LOG_FORMAT = LEVEL + ("%(message)s")

def configure_logging(log, level=None, verbose=False, colour=True):
    '''Turn on logging and add a handler which writes to stderr
    '''
    if level:
        log.setLevel(level.upper() if not isinstance(level, int) else level)

    if verbose:
        LOG_FORMAT=VERBOSE_LOG_FORMAT
    else:
        LOG_FORMAT=SHORT_LOG_FORMAT

    # Set up stream handler
    handler = logging.StreamHandler()
    # do colours if we can
    if colour:
        try:
            import colorlog
            fs_colors = {
                'CRITICAL': 'bold_red',
                'ERROR': 'red',
                'WARNING': 'purple',
                'INFO': 'green',
                'DEBUG': 'yellow',
            }
            formatter = colorlog.ColoredFormatter(
                "%(log_color)s" + LOG_FORMAT,
                datefmt=DATE_FORMAT,
                log_colors=fs_colors
            )
        except ImportError:
            logging.warning("Colour logging not supported. Please install"
                            " the colorlog module to enable\n")
            formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    else:
        formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log

def send_email(from_addr, to_addr, subject, body, reply_addr=None, bcc_addrs=None, attachments=[]):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    if reply_addr:
        msg.add_header('reply-to', reply_addr)
    if bcc_addrs:
        to_addrs = [to_addr] + bcc_addrs
    else:
        to_addrs = [to_addr]

    # Build content of the Email
    body_text = MIMEText(body)
    msg.attach(body_text)

    # If attachment defined, add to email
    for attachment in attachments:
        with open(attachment, "rb") as attachment_file:
            msg_attachment = MIMEApplication(attachment_file.read(),Name=os.path.basename(attachment))
            msg_attachment.add_header('Content-Disposition','attachment',filename=os.path.basename(attachment))
            msg.attach(msg_attachment)

    server = smtplib.SMTP(host='ppsw.cam.ac.uk', port=25)
    server.sendmail(from_addr, to_addrs, msg.as_string())
    server.quit()

def strip_ansi_escape(input_string):
    """
    'ansi_strip'

    This function simply takes a string and removes all ANSI escape codes
    from it.
    """

    ansi_escape_regex = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape_regex.sub('',input_string)


def colorize_str(input_string, colour, style='NORMAL'):
    return f"{getattr(Fore, colour.upper())}{getattr(Style,style.upper())}{input_string}{Style.RESET_ALL}"

def colorize_array(input_array, colour, style='NORMAL'):
    return [colorize_str(str(x), colour, style) for x in input_array]

def truncate_string(input_string, max_length, trailing_suffix=''):
    value = input_string
    truncated_value = (value[:max_length] + trailing_suffix) if len(value) > max_length else value
    return truncated_value

def required_length(nmin,nmax):
    """
    Argparse custom action to support variable number of arguments, i.e: 1 to 3
    See: https://stackoverflow.com/a/4195302
    """
    class RequiredLength(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            if not nmin<=len(values)<=nmax:
                msg='argument "{f}" requires between {nmin} and {nmax} arguments'.format(
                    f=self.dest,nmin=nmin,nmax=nmax)
                raise argparse.ArgumentTypeError(msg)
            setattr(args, self.dest, values)
    return RequiredLength

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":"yes",   "y":"yes",  "ye":"yes",
             "no":"no",     "n":"no"}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while 1:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return default
        elif choice in valid.keys():
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")
