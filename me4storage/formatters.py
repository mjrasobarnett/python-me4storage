import logging
import os
import json
import re
from datetime import datetime
from colorama import Fore, Style

logger = logging.getLogger(__name__)

def format_certificates(system, certificates, detailed=False):
    output = []
    output.append(f"{Fore.WHITE}{Style.BRIGHT}System: {system.system_name}{Style.RESET_ALL}")
    output.append("")

    for certificate in certificates:
        output.append(f"{Fore.WHITE}{Style.BRIGHT}Controller: {certificate.controller} "
                      f"- {certificate.certificate_status}{Style.RESET_ALL}")
        output.append(f"Date added: {certificate.certificate_time}")
        output.append(f"Signature:  {certificate.certificate_signature}")
        if detailed:
            output.append("")
            output.append(re.sub(r'(\s{3,})', r'\n\1', certificate.certificate_text))

        output.append("")


    return "\n".join(output)
