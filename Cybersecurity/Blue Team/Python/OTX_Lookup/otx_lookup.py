#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Ownership, licensing and usage documentation
# can be found at the bottom of this script.

import re
from argparse import ArgumentParser
from rich import print as rprint, pretty
from rich.progress import Progress
import requests


pretty.install()

# ----------------------------------------------------- #


def register_arguments():
    ''' Registers the arguments for the script.'''
    arguments_parser = ArgumentParser(
        description='Utility script to check ip/domains for AlienVault OTX Pulses.')

    arguments_parser.add_argument(
        "-i", "--ip", help='IP to check for pulses.', dest="ip")
    arguments_parser.add_argument(
        "-d", "--domain", help='Domain to check for pulses.', dest="domain")
    arguments_parser.add_argument("-m", "--markdown", help='Export in Markdown format.', dest="markdown", action='store_true')
    arguments_parser.add_argument("-q", "--quiet", help="Does not print to console.", dest="quiet", action='store_true')
    arguments_parser.add_argument(
        "-a", "--apikey", help='API key for AlienVaultOTX', dest="api_key")

    return arguments_parser.parse_args()


def check_ip_for_pulses(ip_address, api_key):
    '''Sends an API request to OTX with an IP address to check for pulses.'''

    with Progress(transient=True) as ip_check_progress:
        ip_task = ip_check_progress.add_task("IP Check:", total=10)

        endpoint = f"https://otx.alienvault.com/api/v1/indicators/IPv4/{ip_address}/general"
        headers = {'X-OTX-API-KEY': f'{api_key}'}
        ip_check_progress.update(ip_task, advance=2)

        res = requests.get(endpoint, headers=headers)
        ip_check_progress.update(ip_task, advance=4)

        if(res.status_code == 200):
            ip_check_progress.update(ip_task, advance=2)

            return res.json()
        else:
            ip_check_progress.update(ip_task, advance=2)

            return False


def check_domain_for_pulses(domain_name, api_key):
    '''Sends an API request to OTX with a domain name to check for pulses.'''

    with Progress(transient=True) as domain_check_progress:
        domain_task = domain_check_progress.add_task("Domain Check:", total=10)

        endpoint = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain_name}/general"
        headers = {'X-OTX-API-KEY': f'{api_key}'}
        domain_check_progress.update(domain_task, advance=2)

        res = requests.get(endpoint, headers=headers)
        domain_check_progress.update(domain_task, advance=4)

        if(res.status_code == 200):
            domain_check_progress.update(domain_task, advance=2)

            return res.json()
        else:
            domain_check_progress.update(domain_task, advance=2)

            return False


def convert_rich_to_markdown(string):
    '''Converts text formatted with the rich library into alternative markdown formatting.'''
    data = str(string)

    patterns = {
        r'\[bold\]': '\n**',
        r'\[\/bold\]': '**',
        r'\[bold black on green blink\]': '\n***',
        r'\[\/bold black on green blink\]': '***',
        r'\[bold italic\]': '\n## ',
        r'\[\/bold italic\]': '',
        # Converts a link with the contents intact.
        r'\[link=(.*?)\]\1\[\/link\]': r'\n[\1](\1)',
    }

    for pattern in patterns:
        data = re.sub(pattern, patterns[pattern], data)

    return data


def parse_pulse_response(data, arg):
    '''Parses the response data from the API.'''

    pulse_info = data['pulse_info']

    malware_families = []
    output = []

    divider = "\n----"

    f_pulse_header = f"[bold italic]Pulse Information for {arg}[/bold italic]"

    f_count = "[bold]Count[/bold]"
    count = pulse_info['count']

    output.append(f_pulse_header)
    output.append(f_count)
    output.append(count)

    for pulse in pulse_info['pulses']:
        f_pulse = "[bold]Pulse[/bold]"
        pulse_name = pulse['name']

        output.append(f_pulse)
        output.append(pulse_name)

        if(pulse['description']):
            f_pulse_description_header = "[bold]Description[/bold]"
            pulse_description = pulse['description']

            output.append(f_pulse_description_header)
            output.append(pulse_description)

        if(pulse['author']):
            f_pulse_author_header = "[bold]Author[/bold]"
            pulse_author = pulse['author']['username']

            output.append(f_pulse_author_header)
            output.append(pulse_author)

        output.append(divider)

    f_pulse_additional_details_header = "[bold italic]Additional Details[/bold italic]"

    output.append(f_pulse_additional_details_header)

    if(pulse_info['related']):
        for group in pulse_info['related']:

            if(pulse_info['related'][group]['malware_families']):
                f_pulse_associated_malware_families_header = "[bold]Associated Malware families[/bold]"

                output.append(f_pulse_associated_malware_families_header)

                for malware in pulse_info['related'][group]['malware_families']:
                    malware_families.append(malware)

                    f_pulse_malware = f"- {malware}"

                    output.append(f_pulse_malware)

    if(pulse_info['references']):
        f_pulse_references_header = "[bold]References[/bold]"

        output.append(f_pulse_references_header)

        for reference in pulse_info['references']:
            f_reference = f'[link={reference}]{reference}[/link]'

            output.append(f_reference)

    return output


def run_pulse_check(arg):
    '''Evaluates the provided arguments and starts the relevant pulse checks.'''
    if(arg == args.domain):
        data = check_domain_for_pulses(args.domain, args.api_key)

    elif(arg == args.ip):
        data = check_ip_for_pulses(args.ip, args.api_key)

    else:
        data = False

    rprint("")

    if(data is False):
        output = ""
        response = '[bold black on red blink]:warning: Failed to get valid response! [/bold black on red blink]'

    else:
        output = parse_pulse_response(data, arg)
        response = f'[bold black on green blink]Successfully retrieved data on {arg}[/bold black on green blink]'

    if(args.quiet is False):
        if(args.markdown):

            rprint(convert_rich_to_markdown(response))
            for line in output:
                rprint(convert_rich_to_markdown(line))

        else:
            rprint(response)
            for line in output:
                rprint(line)

    return output


def export_results(data, filename):
    '''Exports the results of the pulses to a markdown file.'''

    if(args.markdown):

        with open(filename, encoding='utf-8') as file:
            for line in data:
                file.write(convert_rich_to_markdown(line) + "\n")

# ----------------------------------------------------- #


args = register_arguments()


def main():
    '''The main function of the script.'''

    if(args.api_key is None):
        rprint(
            '[bold black on red blink]:warning: No API Key provided! Exiting... [/bold black on red blink]')
        exit()

    if(args.ip is not None):
        rprint(f'Checking IP data for {args.ip}')
        check_data = run_pulse_check(args.ip)
        export_results(check_data, filename=f'ip_{args.ip}.md')

    if(args.domain is not None):
        rprint(f'Checking domain data for {args.domain}...')
        check_data = run_pulse_check(args.domain)
        export_results(check_data, filename=f'domain_{args.domain}.md')

    f_completed_pulse = "[bold black on green blink]Enrichment complete.[/bold black on green blink]"
    if(args.quiet is False):
        if(args.markdown):
            rprint(convert_rich_to_markdown(f_completed_pulse))
        else:
            rprint(f_completed_pulse)
    exit()


if __name__ == "__main__":
    main()

# ------------------------------------------------- #

"""
@Author = "Shrike InfoSec"
@Licence = "MIT"
@Version = "1.0.0"
@Email = "shrike@shrikeinfosec.org"
@Status = "In Development"
"""

""" otx_lookup.py: A utility script to check ip/domains for AlienVault OTX Pulses.

    An API key *MUST* be provided - you can register for one at https://otx.alienvault.com/api 
    and signing-up for an account.

Examples:

    Look up a single IP:

        $ python otx_lookup.py -i 1.1.1.1 -a <API_KEY>

    Look up a single IP without printing to the console:

        $ python otx_lookup.py -i 1.1.1.1 -a <API_KEY> -q
    
    Lookup a domain:

        $ python otx_lookup.py -d google.com -a <API_KEY>
    
    Lookup a domain and export the results to a .md file:
    * In future, this will support an optional -f flag for a filename to be specified.

        $ python otx_lookup.py -d google.com -a <API_KEY> -m
    
Todo:
    * Implement the -f argument to specify a filename for an exported markdown file.
    * Add support for multiple IP addresses or domains read from a text file.

"""
