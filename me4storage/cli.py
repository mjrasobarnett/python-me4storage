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
from me4storage.commands import add, check, modify, show, configure
from me4storage.commands import delete, save, update, restart, email, jira

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
    logger.setLevel(logging.INFO)
    # Set paramiko logger to WARNING level because paramiko logging is quite noisy
    # for our purposes, with many things (like authentication banner) logged to
    # level INFO, which I prefer not to see
    logging.getLogger("paramiko").setLevel(logging.WARNING)
    if args.quiet:
        logger.setLevel(logging.WARN)
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logging.getLogger("paramiko").setLevel(logging.DEBUG)

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
        logger.debug('Found configuration files: {}'.format(config_files))
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
                '-H','--api-host',
                default='localhost',
                help="Controller hostname/IP"
                )
    auth_group.add_argument(
                '--secondary-host',
                help="Secondary controller hostname/IP"
                )
    auth_group.add_argument(
                '-P','--api-port',
                default='443',
                help="API Port"
                )
    auth_group.add_argument(
                '--sftp-port',
                default='1022',
                help="SFTP service port"
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


    email_p = argparse.ArgumentParser(add_help=False)
    email_group = email_p.add_argument_group('Email')
    email_group.add_argument(
                '--recipient',
                dest='email_recipient',
                help='Email Address to send to',
                )
    email_group.add_argument(
                '--sender',
                dest='email_sender',
                help='Email Address to send from',
                )
    email_group.add_argument(
                '--prefix',
                dest='email_prefix',
                default='Storage INFO',
                help='Email Address to send from',
                )

    jira_p = argparse.ArgumentParser(add_help=False)
    jira_group = jira_p.add_argument_group('jira')
    jira_group.add_argument(
                '--jira-server',
                dest='jira_server',
                help='jira server to connect to',
                )
    jira_group.add_argument(
                '--jira-user',
                dest='jira_user',
                help='jira username to connect with',
                )
    jira_group.add_argument(
                '--jira-password',
                dest='jira_password',
                help='jira password to connect with',
                )
    jira_group.add_argument(
                '--jira-issue-id',
                dest='jira_issue_id',
                help='Prefix to prepend to new jira issues created',
                )
    jira_group.add_argument(
                '--jira-prefix',
                dest='jira_prefix',
                default='Storage ALERT',
                help='Prefix to prepend to new jira issues created',
                )
    jira_group.add_argument(
                '--jira-project',
                dest='jira_project',
                default='FAULT',
                help='Jira project to create new jira issues under',
                )
    jira_group.add_argument(
                '--jira-issue-type',
                dest='jira_issue_type',
                default='Fault',
                help='Jira issue type to create new issues as',
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

    check_firmware_p = check_subcommands.add_parser(name='firmware',
                    parents=[auth_p],
                    help='''check firmware version''')
    subparsers.append(check_firmware_p)
    check_firmware_p.set_defaults(func=commands.check.firmware_version)
    check_firmware_p.add_argument(
                '--firmware-version',
                required=True,
                help='Expected Firmware bundle version for controllers'
                )

    ####################################################################
    # ADD subcommands
    ####################################################################

    # Top level subcommand
    add_p = subcommands.add_parser(name='add',
        help='''add commands''')
    add_subcommands = add_p.add_subparsers(dest='add_subcommands',
        title='subcommands of add',description='''
        Below are the core subcommands of program:''')
    add_subcommands.required = True

    add_user_p = add_subcommands.add_parser(name='user',
                    parents=[auth_p],
                    help='''add user''')
    subparsers.append(add_user_p)
    add_user_p.set_defaults(func=commands.add.user)
    add_user_p.add_argument(
                '--username',
                required=True,
                help="User name"
                )
    add_user_p.add_argument(
                '--password',
                required=True,
                help="User password"
                )
    add_user_p.add_argument(
                '--interfaces',
                choices=['cli','wbi','ftp','smis','snmpuser','snmptarget','none'],
                nargs='+',
                help="Connection interfaces this user can access the area over"
                )
    add_user_p.add_argument(
                '--roles',
                choices=['monitor','manage','diagnostic'],
                nargs='+',
                help="User roles"
                )
    add_user_p.add_argument(
                '--timeout',
                default='1800',
                help="Timeout value in seconds"
                )
    add_user_p.add_argument(
                '--base',
                choices=['2','10'],
                default='2',
                help="Sets the display of storage size to be either base2 or base10"
                )

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

    set_user_p = set_subcommands.add_parser(name='user',
                    parents=[auth_p],
                    help='''set user parameters''')
    subparsers.append(set_user_p)
    set_user_p.set_defaults(func=commands.modify.user)
    set_user_p.add_argument(
                '--username',
                required=True,
                help="User name"
                )
    set_user_p.add_argument(
                '--password',
                help="User password"
                )
    set_user_p.add_argument(
                '--interfaces',
                choices=['cli','wbi','ftp','smis','snmpuser','snmptarget','none'],
                nargs='+',
                help="Connection interfaces this user can access the area over"
                )
    set_user_p.add_argument(
                '--roles',
                choices=['monitor','manage','diagnostic'],
                nargs='+',
                help="User roles"
                )
    set_user_p.add_argument(
                '--timeout',
                default='1800',
                help="Timeout value in seconds"
                )
    set_user_p.add_argument(
                '--base',
                choices=['2','10'],
                default='2',
                help="Sets the display of storage size to be either base2 or base10"
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

    set_advanced_settings_p = set_subcommands.add_parser(name='advanced-settings',
                    parents=[auth_p],
                    help='''set advanced_settings notification parameters''')
    subparsers.append(set_advanced_settings_p)
    set_advanced_settings_p.set_defaults(func=commands.modify.advanced_settings)
    set_advanced_settings_p.add_argument(
                '--background-scrub-interval',
                default=None,
                help="Sets the interval in hours between background disk-group scrub"
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

    show_users_p = show_subcommands.add_parser(name='users',
                    parents=[auth_p],
                    help='''show users''')
    subparsers.append(show_users_p)
    show_users_p.set_defaults(func=commands.show.users)

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

    show_hosts_p = show_subcommands.add_parser(name='hosts',
                    parents=[auth_p],
                    help='''show hosts information ''')
    subparsers.append(show_hosts_p)
    show_hosts_p.set_defaults(func=commands.show.hosts)

    show_mappings_p = show_subcommands.add_parser(name='mappings',
                    parents=[auth_p],
                    help='''show mappings information ''')
    subparsers.append(show_mappings_p)
    show_mappings_p.set_defaults(func=commands.show.mappings)
    show_mappings_p.add_argument(
                '--ansible-dm-multipath',
                action='store_true',
                help="Format mappings into format compatible with ansible-dm-multipath"
                )

    show_svc_tag_p = show_subcommands.add_parser(name='svc-tag',
                    aliases=['service-tag'],
                    parents=[auth_p],
                    help='''show svc tag information ''')
    subparsers.append(show_svc_tag_p)
    show_svc_tag_p.set_defaults(func=commands.show.svc_tag)

    show_disks_p = show_subcommands.add_parser(name='disks',
                    parents=[auth_p],
                    help='''show disks information ''')
    subparsers.append(show_disks_p)
    show_disks_p.set_defaults(func=commands.show.disks)
    show_disks_p.add_argument(
                '--detailed',
                action='store_true',
                help="Show more detailed information"
                )

    show_versions_p = show_subcommands.add_parser(name='versions',
                    parents=[auth_p],
                    help='''show versions information ''')
    subparsers.append(show_versions_p)
    show_versions_p.set_defaults(func=commands.show.versions)

    show_certificates_p = show_subcommands.add_parser(name='certificates',
                    aliases=['certificate'],
                    parents=[auth_p],
                    help='''show certificates information ''')
    subparsers.append(show_certificates_p)
    show_certificates_p.set_defaults(func=commands.show.certificates)
    show_certificates_p.add_argument(
                '--detailed',
                action='store_true',
                help="Show more detailed information"
                )

    show_configuration_p = show_subcommands.add_parser(name='configuration',
                    aliases=['certificate'],
                    parents=[auth_p],
                    help='''show configuration information ''')
    subparsers.append(show_configuration_p)
    show_configuration_p.set_defaults(func=commands.show.configuration)

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

    me4024_linear_layout_p = layout_subcommands.add_parser(name='me4024-linear-raid10',
                    parents=[auth_p],
                    help='''Configures ME4084 disk groups using typical '''
                         '''layout for Lustre MDTs - Provisions 2x 10-disk '''
                         '''Linear raid10 volumes''')
    subparsers.append(me4024_linear_layout_p)
    me4024_linear_layout_p.set_defaults(func=commands.configure.disk_layout_me4024_linear_raid10)

    me4024_virtual_layout_p = layout_subcommands.add_parser(name='me4024-virtual-raid10',
                    parents=[auth_p],
                    help='''Configures ME4084 disk groups using typical '''
                         '''layout for Lustre MDTs - Provisions 2x 10-disk '''
                         '''virtual raid10 volumes''')
    subparsers.append(me4024_virtual_layout_p)
    me4024_virtual_layout_p.set_defaults(func=commands.configure.disk_layout_me4024_virtual_raid10)
    me4024_virtual_layout_p.add_argument(
                '--mdt-size',
                type=int,
                required=True,
                help="Size of the MDT volume to create in GiB"
                )
    me4024_virtual_layout_p.add_argument(
                '--mgt-size',
                type=int,
                required=False,
                help="Optional, size of the MDT volume to create in GiB"
                )

    configure_host_p = configure_subcommands.add_parser(name='host',
                    parents=[auth_p],
                    help='''show hosts information ''')
    subparsers.append(configure_host_p)
    configure_host_p.set_defaults(func=commands.configure.host)
    configure_host_p.add_argument(
                '--host-group',
                default=None,
                help="Name of host-group to attach host to. Will "
                     "create hostgroup with default name if not defined."
                )
    configure_host_p.add_argument(
                'name',
                help="Name of host"
                )
    configure_host_p.add_argument(
                '--port-wwpn',
                required=True,
                nargs='+',
                help="List of initiator ports to attach to host"
                )

    configure_mapping_p = configure_subcommands.add_parser(name='mapping',
                    parents=[auth_p],
                    help='''configure volume mappings''')
    subparsers.append(configure_mapping_p)
    configure_mapping_p.set_defaults(func=commands.configure.mapping)
    configure_mapping_g = configure_mapping_p.add_mutually_exclusive_group(required=True)
    configure_mapping_g.add_argument(
                '--all',
                action='store_true',
                dest='all_initiators',
                help="Map volume to all initiators"
                )
    configure_mapping_g.add_argument(
                '--host-group',
                default=None,
                help="Name of host-group to map volumes to."
                )

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

    delete_configuration_p = delete_subcommands.add_parser(name='configuration',
                    parents=[auth_p],
                    help='''Delete all configuration, including storage''')
    subparsers.append(delete_configuration_p)
    delete_configuration_p.set_defaults(func=commands.delete.configuration)

    delete_host_configuration_p = delete_subcommands.add_parser(name='host-configuration',
                    parents=[auth_p],
                    help='''Delete all host configuration''')
    subparsers.append(delete_host_configuration_p)
    delete_host_configuration_p.set_defaults(func=commands.delete.host_configuration)

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

    delete_host_group_p = delete_subcommands.add_parser(name='host-group',
                    parents=[auth_p],
                    help='''Delete host group''')
    subparsers.append(delete_host_group_p)
    delete_host_group_p.set_defaults(func=commands.delete.host_group)
    delete_host_group_p.add_argument(
                '--delete-hosts',
                action='store_true',
                default=None,
                dest='delete_host_group_hosts',
                help="Also delete all hosts in the group"
                )

    delete_host_group_g = delete_host_group_p.add_mutually_exclusive_group(required=True)
    delete_host_group_g.add_argument(
                '--name',
                required=False,
                nargs='*',
                default=None,
                dest='delete_host_group_names',
                help="hosts to delete"
                )
    delete_host_group_g.add_argument(
                '--all',
                action='store_true',
                dest='delete_host_group_all',
                help="Delete all host groups present"
                )

    delete_mapping_p = delete_subcommands.add_parser(name='mapping',
                    parents=[auth_p],
                    help='''Delete volume mapping''')
    subparsers.append(delete_mapping_p)
    delete_mapping_p.set_defaults(func=commands.delete.mapping)
    delete_mapping_volumes_g = delete_mapping_p.add_mutually_exclusive_group(required=True)
    delete_mapping_volumes_g.add_argument(
                '--volume',
                dest='delete_mapping_volume',
                help="Name of volume to un-map"
                )
    delete_mapping_volumes_g.add_argument(
                '--all',
                action='store_true',
                dest='delete_mapping_all_volumes',
                help="Delete mapping for all volumes"
                )
    delete_mapping_hosts_g = delete_mapping_p.add_mutually_exclusive_group(required=True)
    delete_mapping_hosts_g.add_argument(
                '--host',
                dest='delete_mapping_host',
                help="Name of host to un-map volumes from"
                )
    delete_mapping_hosts_g.add_argument(
                '--host-group',
                dest='delete_mapping_host_group',
                help="Name of host-group to un-map volumes from"
                )

    ####################################################################
    # SAVE subcommands
    ####################################################################

    # Top level subcommand
    save_p = subcommands.add_parser(name='save',
        help='''save commands''')
    save_subcommands = save_p.add_subparsers(dest='save_subcommands',
        title='subcommands of save',description='''
        Below are the core subcommands of program:''')
    save_subcommands.required = True

    save_logs_p = save_subcommands.add_parser(name='logs',
                    parents=[auth_p],
                    help='''save logs''')
    subparsers.append(save_logs_p)
    save_logs_p.set_defaults(func=commands.save.logs)
    save_logs_p.add_argument(
                '--output-dir',
                default=None,
                help="Name of output directory to save logs file to"
                )
    save_logs_p.add_argument(
                '--output-file',
                default=None,
                help="Name of output file to save logs to"
                )

    ####################################################################
    # UPDATE subcommands
    ####################################################################

    # Top level subcommand
    update_p = subcommands.add_parser(name='update',
        help='''update commands''')
    update_subcommands = update_p.add_subparsers(dest='update_subcommands',
        title='subcommands of update',description='''
        Below are the core subcommands of program:''')
    update_subcommands.required = True

    update_firmware_p = update_subcommands.add_parser(name='controller-firmware',
                    parents=[auth_p],
                    help='''update controller-firmware''')
    subparsers.append(update_firmware_p)
    update_firmware_p.set_defaults(func=commands.update.firmware)

    update_firmware_p.add_argument(
                '--force',
                action='store_true',
                help='Proceed with upgrade even if readiness check fails',
                )
    update_firmware_p.add_argument(
                '--controller-firmware',
                required=True,
                help='Zip file containing ME4 '
                'controller firmewarZipfile, or extracted .bin file '
                'containing ME4 controller firmware'
                )

    update_disk_firmware_p = update_subcommands.add_parser(name='disk-firmware',
                    parents=[auth_p],
                    help='''update disk-firmware''')
    subparsers.append(update_disk_firmware_p)
    update_disk_firmware_p.set_defaults(func=commands.update.disk_firmware)

    update_disk_firmware_p.add_argument(
                '--force',
                action='store_true',
                help='Proceed with upgrade even if readiness check fails',
                )
    update_disk_firmware_p.add_argument(
                '--yes',
                action='store_true',
                dest='do_not_prompt',
                help="Don't prompt for confirmation to proceed with update",
                )
    update_disk_firmware_p.add_argument(
                '--disk-firmware',
                required=True,
                help='Zip file containing ME4 disk firmware'
                )

    update_certificate_p = update_subcommands.add_parser(name='certificate',
                    parents=[auth_p],
                    help='''update controller TLS certificate''')
    subparsers.append(update_certificate_p)
    update_certificate_p.set_defaults(func=commands.update.certificate)
    update_certificate_p.add_argument(
                '--tls-certificate', '--certificate',
                required=True,
                help='PEM encoded TLS public cert',
                )
    update_certificate_p.add_argument(
                '--tls-key', '--key',
                required=True,
                help='TLS RSA key',
                )

    ####################################################################
    # EMAIL subcommands
    ####################################################################

    # Top level subcommand
    email_parser_p = subcommands.add_parser(name='email',
        help='''email commands''')
    email_subcommands = email_parser_p.add_subparsers(dest='email_subcommands',
        title='subcommands of email',description='''
        Below are the core subcommands of program:''')
    email_subcommands.required = True

    email_logs_p = email_subcommands.add_parser(name='logs',
                    parents=[auth_p, email_p],
                    help='''email logs''')
    subparsers.append(email_logs_p)
    email_logs_p.set_defaults(func=commands.email.logs)

    ####################################################################
    # JIRA subcommands
    ####################################################################

    # Top level subcommand
    jira_parser_p = subcommands.add_parser(name='jira',
        help='''jira commands''')
    jira_subcommands = jira_parser_p.add_subparsers(dest='jira_subcommands',
        title='subcommands of jira',description='''
        Below are the core subcommands of program:''')
    jira_subcommands.required = True

    jira_logs_p = jira_subcommands.add_parser(name='logs',
                    parents=[auth_p, jira_p],
                    help='''jira logs''')
    subparsers.append(jira_logs_p)
    jira_logs_p.set_defaults(func=commands.jira.logs)

    ####################################################################
    # RESTART subcommands
    ####################################################################

    # Top level subcommand
    restart_p = subcommands.add_parser(name='restart',
        help='''restart commands''')
    restart_subcommands = restart_p.add_subparsers(dest='restart_subcommands',
        title='subcommands of restart',description='''
        Below are the core subcommands of program:''')
    restart_subcommands.required = True

    restart_controller_p = restart_subcommands.add_parser(name='management-controllers',
                    parents=[auth_p],
                    help='''restart management-controllers''')
    subparsers.append(restart_controller_p)
    restart_controller_p.set_defaults(func=commands.restart.management_controllers)
    restart_controller_p.add_argument(
                '--controller',
                choices=['A','B','0','1'],
                help='Choose controller to restart (if not set, will restart both)',
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

        session = Session(host = args.api_host,
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
