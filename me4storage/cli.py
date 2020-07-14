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

from me4storage.api.session import Session
from me4storage import commands
from me4storage.commands import check, modify, show, configure, delete

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
        default=['/etc/me4cli/me4cli.conf','.me4cli.conf'],
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

    ####################################################################
    # SET subcommands
    ####################################################################

    # Top level subcommand
    set_p = subcommands.add_parser(name='set',
        help='''set commands''')
    set_subcommands = set_p.add_subparsers(dest='set_subcommands',
        title='subcommands of set',description='''
        Below are the core subcommands of program:''')
    set_subcommands.required = True

    set_system_info_p = set_subcommands.add_parser(name='system-info',
                    parents=[auth_p],
                    help='''set system information (name, contact, desc)''')
    subparsers.append(set_system_info_p)
    set_system_info_p.set_defaults(func=commands.modify.system_info)
    set_system_info_p.add_argument(
                '--name',
                dest='system_name',
                default=None,
                help="System name"
                )
    set_system_info_p.add_argument(
                '--info',
                dest='system_info',
                default=None,
                help="Description of what the system is used for"
                )
    set_system_info_p.add_argument(
                '--contact',
                dest='system_contact',
                default=None,
                help="System contact information for administrator"
                )
    set_system_info_p.add_argument(
                '--location',
                dest='system_location',
                default=None,
                help="Location of the System"
                )

    set_ntp_p = set_subcommands.add_parser(name='ntp',
                    parents=[auth_p],
                    help='''set ntp parameters''')
    subparsers.append(set_ntp_p)
    set_ntp_p.set_defaults(func=commands.modify.ntp)
    set_ntp_p.add_argument(
                '--status',
                dest="status",
                required=True,
                choices=['enabled','disabled'],
                default=None,
                help="Enable/disable use of NTP"
                )
    set_ntp_p.add_argument(
                '--ntp-server',
                dest='ntp_server',
                required=True,
                default=None,
                help="IP/FQDN of NTP server"
                )
    set_ntp_p.add_argument(
                '--timezone',
                dest='timezone',
                default=None,
                help="Timezone offset, in hours (-12 to +14), from UTC"
                )

    set_dns_p = set_subcommands.add_parser(name='dns',
                    parents=[auth_p],
                    help='''set dns parameters''')
    subparsers.append(set_dns_p)
    set_dns_p.set_defaults(func=commands.modify.dns)
    set_dns_p.add_argument(
                '--name-servers',
                dest='name_servers',
                required=True,
                nargs='*',
                default=None,
                help="Ordered list of name server addresses"
                )
    set_dns_p.add_argument(
                '--search-domains',
                dest='search_domains',
                required=True,
                nargs='*',
                default=None,
                help="Ordered list of search domains"
                )

    set_network_p = set_subcommands.add_parser(name='network',
                    parents=[auth_p],
                    help='''set network parameters''')
    subparsers.append(set_network_p)
    set_network_p.set_defaults(func=commands.modify.network)
    set_network_p.add_argument(
                '--controller-a-ip',
                required=True,
                default=None,
                help="Controller A management IPv4 address"
                )
    set_network_p.add_argument(
                '--controller-b-ip',
                required=True,
                default=None,
                help="Controller B management IPv4 address"
                )
    set_network_p.add_argument(
                '--gateway',
                required=True,
                default=None,
                help="Default Gateway"
                )
    set_network_p.add_argument(
                '--netmask',
                required=True,
                default=None,
                help="Netmask"
                )

    set_support_assist_p = set_subcommands.add_parser(name='support-assist',
                    parents=[auth_p],
                    help='''set support-assist on/off''')
    subparsers.append(set_support_assist_p)
    set_support_assist_p.set_defaults(func=commands.modify.support_assist)
    set_support_assist_p.add_argument(
                '--status',
                required=True,
                choices=['enabled','disabled'],
                default='disabled',
                help="Enable or Disable support-assist functionality (default: %(default)s)"
                )

    set_email_p = set_subcommands.add_parser(name='email',
                    parents=[auth_p],
                    help='''set email notification parameters''')
    subparsers.append(set_email_p)
    set_email_p.set_defaults(func=commands.modify.email)
    set_email_p.add_argument(
                '--domain',
                required=True,
                help="Sender domain"
                )
    set_email_p.add_argument(
                '--recipients',
                required=True,
                nargs='+',
                action=util.required_length(1,4),
                help="Recipient emails for notifications"
                )
    set_email_p.add_argument(
                '--security-protocol',
                default='none',
                choices=['tls','ssl','none'],
                help="SMTP security protocol"
                )
    set_email_p.add_argument(
                '--notification-level',
                default='none',
                choices=['crit','error','warn','resolved','info','none'],
                help="Email notification level"
                )
    set_email_p.add_argument(
                '--port',
                default='25',
                help="SMTP Server port. Default: 25"
                )
    set_email_p.add_argument(
                '--server',
                required=True,
                help="SMTP Server"
                )
    set_email_p.add_argument(
                '--sender',
                required=True,
                default=None,
                help="Sender name, joinged with domain to form the 'from' address"
                )

    ####################################################################
    # SHOW subcommands
    ####################################################################

    # Top level subcommand
    show_p = subcommands.add_parser(name='show',
        help='''show commands''')
    show_subcommands = show_p.add_subparsers(dest='show_subcommands',
        title='subcommands of show',description='''
        Below are the core subcommands of program:''')
    show_subcommands.required = True

    show_system_info_p = show_subcommands.add_parser(name='system-info',
                    parents=[auth_p],
                    help='''show system information (name, contact, desc)''')
    subparsers.append(show_system_info_p)
    show_system_info_p.set_defaults(func=commands.show.system_info)

    show_network_p = show_subcommands.add_parser(name='network',
                    parents=[auth_p],
                    help='''show network information (IP, DNS, NTP)''')
    subparsers.append(show_network_p)
    show_network_p.set_defaults(func=commands.show.network)

    show_notifications_p = show_subcommands.add_parser(name='notifications',
                    parents=[auth_p],
                    help='''show notifications information (email, SNMP, ...)''')
    subparsers.append(show_notifications_p)
    show_notifications_p.set_defaults(func=commands.show.notifications)

    show_storage_p = show_subcommands.add_parser(name='storage',
                    parents=[auth_p],
                    help='''show storage information ''')
    subparsers.append(show_storage_p)
    show_storage_p.set_defaults(func=commands.show.storage)
    show_storage_p.add_argument(
                '--detailed',
                action='store_true',
                help="Show more detailed information"
                )

    ####################################################################
    # CONFIGURE subcommands
    ####################################################################

    # Top level subcommand
    configure_p = subcommands.add_parser(name='configure',
        help='''configure commands''')
    configure_subcommands = configure_p.add_subparsers(dest='configure_subcommands',
        title='subcommands of configure',description='''
        Below are the core subcommands of program:''')
    configure_subcommands.required = True

    layout_p = configure_subcommands.add_parser(name='disk-layout',
        help='''disk-layout commands''')
    layout_subcommands = layout_p.add_subparsers(dest='disk_subcommands',
        title='subcommands of disk-layout',description='''
        Below are subcommands of disk-layout:''')
    layout_subcommands.required = True

    me4084_linear_layout_p = layout_subcommands.add_parser(name='me4084-linear-raid6',
                    parents=[auth_p],
                    help='''Configures ME4084 disk groups using typical '''
                         '''layout for Lustre OSTs - Provisions 8x 10-disk '''
                         '''Linear Raid6 volumes with a 1MiB stripe-width.''')
    subparsers.append(me4084_linear_layout_p)
    me4084_linear_layout_p.set_defaults(func=commands.configure.disk_layout_me4084_linear_raid6)

    ####################################################################
    # DELETE subcommands
    ####################################################################

    # Top level subcommand
    delete_p = subcommands.add_parser(name='delete',
        help='''delete commands''')
    delete_subcommands = delete_p.add_subparsers(dest='delete_subcommands',
        title='subcommands of delete',description='''
        Below are the core subcommands of program:''')
    delete_subcommands.required = True

    delete_pool_p = delete_subcommands.add_parser(name='pool',
                    parents=[auth_p],
                    help='''Delete pool''')
    subparsers.append(delete_pool_p)
    delete_pool_p.set_defaults(func=commands.delete.pool)

    delete_pool_g = delete_pool_p.add_mutually_exclusive_group(required=True)
    delete_pool_g.add_argument(
                '--name',
                required=False,
                nargs='*',
                default=None,
                dest='delete_pool_names',
                help="Pools to delete"
                )
    delete_pool_g.add_argument(
                '--all',
                action='store_true',
                dest='delete_pool_all',
                help="Delete all pools present"
                )

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

        session = Session(baseurl = args.api_baseurl,
                          port = args.api_port,
                          username = args.api_username,
                          password = args.api_password,
                          verify = False if args.api_disable_tls_verification else True)
        rc = args.func(args, session)
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
