import logging
import colorama
from colorama import Fore, Style
from terminaltables import SingleTable
from pprint import pformat
import datetime
import os
import time
import re
import tempfile
from zipfile import ZipFile
import pysftp

from fuzzywuzzy import fuzz

from me4storage.api.session import Session
from me4storage.common.exceptions import ApiError
from me4storage.common.nsca import CheckResult
import me4storage.common.util as util
import me4storage.common.tables as tables
import me4storage.common.formatters
import me4storage.formatters as formatters

from me4storage.api import show, check, restart
import me4storage.common.tables as tables

logger = logging.getLogger(__name__)

def firmware(args, session):
    force_update = args.force
    firmware_bundle = args.controller_firmware

    if not os.path.isfile(firmware_bundle):
        logger.error(f"Firmware file {firmware_bundle} not found. Aborting...")
        return CheckResult.CRITICAL.value

    user = next(iter(show.users(session, user=args.api_username)),None)
    if user and not user.ftp_enabled:
        logger.error(f"User '{args.api_username}' not enabled for FTP access. Aborting...")
        return CheckResult.CRITICAL.value

    systems = show.system(session)
    for system in systems:
        # As per, 'Best practices for firmware update (https://www.dell.com/support/manuals/uk/en/ukbsdt1/powervault-me4084/me4_series_ag_pub/best-practices-for-firmware-update?guid=guid-17a809b7-f38d-41e5-8892-e3f5ed3babb4&lang=en-us)
        # we first check the system's readiness for firmware upgrade
        # If this fails, and we haven't given the 'force' flag as an argument
        # then we abort the process at this stage
        readiness = check.firmware_upgrade_health(session)[0]
        if readiness.overall_health_numeric is not 0:
            if force_update:
                reasons = [ "  - " + reason.readiness_reason for reason in readiness.code_load_readiness_reasons]
                logger.warn(f"System: {system.system_name} has failed readiness "
                            f"check for Firmware upgrade.\n"
                            f"Overall Health: {readiness.overall_health}\n"
                            f"Reasons:\n" + "\n".join(reasons))
                logger.warning(f"Force flag was provided, ignoring...\n")
            else:
                reasons = [ "  - " + reason.readiness_reason for reason in readiness.code_load_readiness_reasons]
                logger.error(f"System: {system.system_name} has failed readiness "
                             f"check for Firmware upgrade. Aborting...\n"
                             f"Overall Health: {readiness.overall_health}\n"
                             f"Reasons:\n" + "\n".join(reasons))
                rc = CheckResult.CRITICAL
                return rc.value
        else:
            logger.info(f"System: {system.system_name} has passed "
                         f"readiness check for Firmware upgrade. Proceeding...")


        # Next we check for any unwritable data in the cache
        caches = show.unwritable_cache(session)
        for cache in caches:
            if cache.has_unwritable_data:
                logger.error(f"System: {system.system_name} has unwritable "
                             f"data in the controller cache. Aborting...\n"
                             f"  Controller a: {cache.unwritable_a_percentage}%\n"
                             f"  Controller b: {cache.unwritable_b_percentage}%")
                return CheckResult.CRITICAL.value

        logger.info(f"Controllers have passed check for unwritable data in cache. Proceeding...")


    with tempfile.TemporaryDirectory() as tmpdirname:
        logger.info(f'Extracting firmware bundle {firmware_bundle}')
        with ZipFile(firmware_bundle, 'r') as zipobj:
            list_of_files = zipobj.namelist()
            # We only expect a single file to be present, extract the first
            # file we come across in the bundle ending in '.bin'
            firmware_file = next((filename for filename in list_of_files if filename.endswith('.bin')), None)
            if firmware_file is None:
                logger.error("No files ending in '.bin' found in firmware bundle")
                return CheckResult.CRITICAL.value

            logger.info(f'Extracting firmware file to {tmpdirname}/{firmware_file}')
            firmware_path = zipobj.extract(firmware_file, path=tmpdirname)

            version_regex = re.compile(
                        r"^(?P<bundle_version>[\w-]+)"
                        r"-"
                        r"dellemc.bin$"
                        )
            match = re.search(version_regex, firmware_file)
            if not match:
                logger.error("Failed to parse Firmware version from filename.")
                return CheckResult.CRITICAL.value

            bundle_version = match.group('bundle_version')

            logger.info(f"Uploading firmware version: {bundle_version}")
            cnopts = pysftp.CnOpts(knownhosts=os.path.expanduser(os.path.join('~','.ssh','known_hosts')))
            cnopts.hostkeys = None
            with pysftp.Connection(args.api_host,
                              port=int(args.sftp_port),
                              username=args.api_username,
                              password=args.api_password,
                              cnopts=cnopts,
                              ) as sftp:
                sftp.put(firmware_path, remotepath="/flash", confirm=False)

            logger.info("Upload complete. Firmware update happens asynchronously in the background. "
                        "Update can take from 10-20 minutes to complete.")

    return CheckResult.OK.value

def disk_firmware(args, session):
    force_update = args.force
    firmware_bundle = args.disk_firmware

    if not os.path.isfile(firmware_bundle):
        logger.error(f"Firmware file {firmware_bundle} not found. Aborting...")
        return CheckResult.CRITICAL.value

    user = next(iter(show.users(session, user=args.api_username)),None)
    if user and not user.ftp_enabled:
        logger.error(f"User '{args.api_username}' not enabled for FTP access. Aborting...")
        return CheckResult.CRITICAL.value

    systems = show.system(session)
    for system in systems:
        # As per, 'Best practices for firmware update
        # (https://www.dell.com/support/manuals/uk/en/ukbsdt1/powervault-me4084/me4_series_ag_pub/best-practices-for-firmware-update?guid=guid-17a809b7-f38d-41e5-8892-e3f5ed3babb4&lang=en-us)
        # we first check the system's readiness for firmware upgrade
        # If this fails, and we haven't given the 'force' flag as an argument
        # then we abort the process at this stage
        readiness = check.firmware_upgrade_health(session)[0]
        if readiness.overall_health_numeric is not 0:
            if force_update:
                reasons = [ "  - " + reason.readiness_reason for reason in readiness.code_load_readiness_reasons]
                logger.warn(f"System: {system.system_name} has failed readiness "
                            f"check for Firmware upgrade.\n"
                            f"Overall Health: {readiness.overall_health}\n"
                            f"Reasons:\n" + "\n".join(reasons))
                logger.warning(f"Force flag was provided, ignoring...\n")
            else:
                reasons = [ "  - " + reason.readiness_reason for reason in readiness.code_load_readiness_reasons]
                logger.error(f"System: {system.system_name} has failed readiness "
                             f"check for Firmware upgrade. Aborting...\n"
                             f"Overall Health: {readiness.overall_health}\n"
                             f"Reasons:\n" + "\n".join(reasons))
                rc = CheckResult.CRITICAL
                return rc.value
        else:
            logger.info(f"System: {system.system_name} has passed "
                         f"readiness check for Firmware upgrade. Proceeding...")


        # Next we check for any unwritable data in the cache
        caches = show.unwritable_cache(session)
        for cache in caches:
            if cache.has_unwritable_data:
                logger.error(f"System: {system.system_name} has unwritable "
                             f"data in the controller cache. Aborting...\n"
                             f"  Controller a: {cache.unwritable_a_percentage}%\n"
                             f"  Controller b: {cache.unwritable_b_percentage}%")
                return CheckResult.CRITICAL.value

        logger.info(f"Controllers have passed check for unwritable data in cache. Proceeding...")


    with tempfile.TemporaryDirectory() as tmpdirname:
        logger.info(f'Extracting firmware bundle {firmware_bundle}')
        with ZipFile(firmware_bundle, 'r') as zipobj:
            list_of_files = zipobj.namelist()
            # We only expect a single file to be present, extract the first
            # file we come across in the bundle ending in '.bin'
            valid_extensions = [".bin", '.BIN', '.lod', '.LOD']
            new_firmware_files = [filename for filename in list_of_files if filename.endswith(tuple(valid_extensions))]
            logger.debug("New firmware files: {new_firmware_files}")
            disks = show.disks(session)
            # Get list of all unique firmware versions + vendor
            current_firmware_versions = []
            for disk in disks:
                current_firmware = f"{disk.vendor}/{disk.revision}"
                if current_firmware not in current_firmware_versions:
                    current_firmware_versions.append(current_firmware)

            logger.debug(f"Current firmware revisions: {current_firmware_versions}")
            updateable_firmware_files = []
            for current_firmware in current_firmware_versions:
                # Check if current firmware exists in new_firmware_files
                # Note we need to remove the firmware file extension, and
                # transform everything to lowercase for comparision
                if current_firmware.lower() in [os.path.splitext(new_firmware)[0].lower() for new_firmware in new_firmware_files]:
                    # If so, move on, we must be at the latest firmware version for this model
                    continue
                else:
                    # For each new firmware file in the bundle, we calculate
                    # the Levenshtein ratio using the 'fuzzywuzzy' package
                    # https://github.com/seatgeek/fuzzywuzzy
                    # to determine if the new firmware file is a related firmware
                    # version of the current firmware.
                    #
                    # Firmware versions should only differ by 1 character most of the time
                    # eg: NS06 vs NS07 or NSF2 vs NSF3
                    #
                    # therefore the Levenshtein ratio should be very high
                    # for a related firmware package. We will take as a cutoff
                    # a value of 95 needed to indicate that two firmware versions
                    # are related
                    for new_firmware_file in new_firmware_files:
                        new_firmware = os.path.splitext(new_firmware_file)[0]
                        # Use 'fuzzywuzzy' to compute the Levenshtein ratio, using a common
                        # prefix to make the computed words longer, to ensure that
                        # the ratio matching for short strings with 1 character
                        # different is above 95% threshold
                        ratio = fuzz.ratio('firmware: ' + new_firmware.lower(), 'firmware: ' + current_firmware.lower())
                        logger.debug(f"Comparing: {current_firmware} vs {new_firmware}. Levenshtein Ratio: {ratio}")
                        if ratio >= 95:
                            updateable_firmware_files.append({'firmware_file': new_firmware_file,
                                                              'new_version': new_firmware,
                                                              'current_version': current_firmware})
                        elif ratio >= 90:
                            logger.warn(f"Firmware: {new_firmware} has a Levenshtein "
                                        f"ratio >= 90 compared to {current_firmware}. "
                                        f"Check this isn't a mistake.")

            if len(updateable_firmware_files) == 0:
                logger.info("No firmware files found newer than current revisions. Aborting...")
                return CheckResult.OK.value

            logger.info(f"Following firmware files found which are newer than current versions present:")
            for entry in updateable_firmware_files:
                logger.info(f"{entry.get('new_version')} is an upgrade for {entry.get('current_version')}. File: {entry.get('firmware_file')}")

            # Check if user wants to proceed with update
            if args.do_not_prompt is False:
                result = util.query_yes_no('Would you like to proceed with the update?', default='no')
                if result == 'no':
                    logger.info(f"Not applying updates. Aborting...")
                    return CheckResult.OK.value

            logger.info(f"Updating all disks with new firmware versions...")
            for entry in updateable_firmware_files:
                logger.info(f"Extracting firmware file to {tmpdirname}/{entry.get('firmware_file')}")
                firmware_path = zipobj.extract(entry.get('firmware_file'), path=tmpdirname)

                logger.info(f"Uploading firmware version: {entry.get('new_version')}")
                cnopts = pysftp.CnOpts(knownhosts=os.path.expanduser(os.path.join('~','.ssh','known_hosts')))
                cnopts.hostkeys = None
                with pysftp.Connection(args.api_host,
                                  port=int(args.sftp_port),
                                  username=args.api_username,
                                  password=args.api_password,
                                  cnopts=cnopts,
                                  ) as sftp:
                    sftp.put(firmware_path, remotepath="/disk", confirm=False)

                logger.info("Upload complete. Firmware update happens asynchronously in the background. "
                            "Update can take a number of minutes to complete.")

    return CheckResult.OK.value

def certificate(args, session):
    cert_file = args.tls_certificate
    key_file = args.tls_key

    if not os.path.isfile(cert_file):
        logger.error(f"TLS cert, {cert_file} not found. Aborting...")
        return CheckResult.CRITICAL.value
    if not os.path.isfile(key_file):
        logger.error(f"TLS key, {key_file} not found. Aborting...")
        return CheckResult.CRITICAL.value

    user = next(iter(show.users(session, user=args.api_username)),None)
    if user and not user.ftp_enabled:
        logger.error(f"User '{args.api_username}' not enabled for FTP access. Aborting...")
        return CheckResult.CRITICAL.value

    if args.secondary_host:
        controller_ips = [args.api_host, args.secondary_host]
    else:
        # Attempt to determine controller IPs
        network_parameters = show.network_parameters(session)
        controller_a = next(iter(network for network in network_parameters if network.controller == 'A'))
        controller_b = next(iter(network for network in network_parameters if network.controller == 'B'))
        controller_ips = [controller_a.ip_address, controller_b.ip_address]

    cnopts = pysftp.CnOpts(knownhosts=os.path.expanduser(os.path.join('~','.ssh','known_hosts')))
    cnopts.hostkeys = None
    for ip in controller_ips:
        logger.info(f"Connecting to: {ip} for certificate upload...")
        with pysftp.Connection(ip,
                          port=int(args.sftp_port),
                          username=args.api_username,
                          password=args.api_password,
                          cnopts=cnopts,
                          ) as sftp:
            logger.info(f"Uploading tls cert: {cert_file}")
            sftp.put(cert_file, remotepath="/cert-file", confirm=False)
            logger.info(f"Uploading tls key: {key_file}")
            sftp.put(key_file, remotepath="/cert-key-file", confirm=False)

    logger.info("Uploads complete. Restarting both management controllers to take effect...")
    restart.mc(session, controller='both')

    # Wait 5 minutes before attempting to start new connections
    time.sleep(300)
    # Establish a new session here, since we have restarted the management
    # ports. Boost the number of retries to catch indeterminate time until it's online
    session = Session(host = args.api_host,
                      port = args.api_port,
                      username = args.api_username,
                      password = args.api_password,
                      verify = False if args.api_disable_tls_verification else True,
                      retries=10,
                      )

    system = next(iter(show.system(session)))
    certificates = show.certificate(session, controller='both')
    print(formatters.format_certificates(system, certificates))

    return CheckResult.OK.value
