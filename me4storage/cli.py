import argparse
import argcomplete
import logging
import configparser
import colorama
import sys
import traceback

from colorama import Fore, Style
from collections import namedtuple

from me4storage.common import util
from me4storage.common.exceptions import UsageError
from me4storage.common.nsca import CheckResult

from me4storage import commands
from me4storage.commands import check

def cli():

    # Parse configuration files present if any to get default values
    # We make this parser with add_help=False so that
    # it doesn't parse -h and print help.
    conf_parser = argparse.ArgumentParser(
        prog='me4cli',
        description='CLI utility around ME4 API',
        # Turn off help, so we print all options in response to -h
        add_help=False,
        )
    conf_parser.add_argument(
        '-f','--config-files',
        nargs='?',
        # Later files take precendence over earlier
        default=['/etc/nstorcli/nstorcli.conf','.nstorcli.conf'],
        help="Tool configuration file location (default: %(default)s)"
        )
    conf_parser.add_argument('--debug',
        action="store_true",
        default=False,
        dest='debug',
        help='Enable debug output')
    conf_parser.add_argument('--quiet',
        action="store_true",
        default=False,
        dest='quiet',
        help='Suppress all informational output, log at WARN level')
    conf_parser.add_argument('--nocolour', '--nocolor',
        action="store_true",
        default=False,
        dest='nocolour',
        help='Strip ANSI color codes from all output to console')
    args, remaining_argv = conf_parser.parse_known_args()

    # Set log level
    logger = logging.getLogger()
    if args.quiet:
        logger.setLevel(logging.WARN)
    if args.debug:
        logger.setLevel(logging.DEBUG)

    # Set up colorama
    if args.nocolour:
        util.configure_logging(logger,colour=False)
        colorama.init(strip=True, autoreset=True)
    else:
        util.configure_logging(logger)
        colorama.init(autoreset=True)

    # Set up configuration file if present
    file_parser = configparser.SafeConfigParser()
    config_files = file_parser.read(args.config_files)
    conf_file_defaults = {}
    if config_files:
        logger.info('Found configuration files: {}'.format(config_files))
        for section_name in file_parser.sections():
            logger.debug('Section: {}'.format(section_name))
            logger.debug('  Options: {}'.format(file_parser.options(section_name)))
            for name, value in file_parser.items(section_name):
                logger.debug('  {} = {}'.format(name, value))
                conf_file_defaults.update({name: value})
    logger.debug("Config File options: {}".format(conf_file_defaults))

    # Create the rest of the parser inheriting from the conf_parser above
    # with all remaining arguments
    parser = argparse.ArgumentParser(
        parents=[conf_parser],
        )
    # Create list to store all subparsers so we can iterate over these
    # to apply command defaults from config
    subparsers = []

    # Define command line interface
    # Set up subparses for the subcommands
    subcommands = parser.add_subparsers(dest='subcommands',
                                        title='subcommands',
                                        description='''
        Below are the core subcommands of program:''')
    subcommands.required = True

    #########
    # COMMON Arguments
    #########
    auth_p = argparse.ArgumentParser(add_help=False)
    subparsers.append(auth_p)
    auth_group = auth_p.add_argument_group('Authentication')
    auth_group.add_argument(
                '-H','--api-baseurl',
                default='https://localhost',
                help="API Base URL"
                )
    auth_group.add_argument(
                '-P','--api-port',
                default='443',
                help="NEF API Port"
                )
    auth_group.add_argument(
                '-u','--api-username',
                default='manage',
                help="API username"
                )
    auth_group.add_argument(
                '-p','--api-password',
                default='',
                help="API password"
                )
    auth_group.add_argument(
                '--api-disable-tls-verification',
                action='store_true',
                help="API disable TLS certificate verification"
                )

    ####################################################################
    # CHECK subcommands
    ####################################################################

    # Top level subcommand
    check_p = subcommands.add_parser(name='check',
        help='''check commands''')
    check_subcommands = check_p.add_subparsers(dest='check_subcommands',
        title='subcommands of check',description='''
        Below are the core subcommands of program:''')
    check_subcommands.required = True

    check_health_p = check_subcommands.add_parser(name='health',
                    parents=[auth_p],
                    help='''check health status''')
    subparsers.append(check_health_p)
    check_health_p.set_defaults(func=commands.check.health_status)

    #########
    # PARSE arguments
    #########
    # Setup bash completion
    argcomplete.autocomplete(parser)
    # Set defaults, using values from conf_parser
    parser.set_defaults(**conf_file_defaults)
    for subparser in subparsers:
        subparser.set_defaults(**conf_file_defaults)

    # Parse arguments
    args = parser.parse_args()

    logger.debug('Command line args: {}'.format(args))

    # Run subcommand function
    try:
        rc = args.func(args)
    except Exception as e:
        # Print traceback if debug flag enabled
        if args.debug:
            logger.error(traceback.format_exc())

        # Print exception message and return error
        logger.error("Exception {}: {}".format(e.__class__.__name__, e))
        sys.exit(CheckResult.CRITICAL.value)

    sys.exit(rc)

########################################################################
### MAIN
########################################################################
if __name__ == '__main__':
    cli()
