#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Ownership, licensing and usage documentation can be found at the bottom of this script.

import re
import requests

from rich import print as rprint, pretty
from rich.progress import Progress
from argparse import ArgumentParser


pretty.install()

# ----------------------------------------------------- #

def registerArguments():
    argumentsParser = ArgumentParser(
        description='Utility script to check ip/domains for AlienVault OTX Pulses.')

    argumentsParser.add_argument(
        "-i", "--ip", help='IP to check for pulses.', dest="ip"),
    argumentsParser.add_argument(
        "-d", "--domain", help='Domain to check for pulses.', dest="domain"),
    argumentsParser.add_argument("-m", "--markdown", help='Export in Markdown format.',
                                 dest="markdown", action='store_true'),
    argumentsParser.add_argument("-q", "--quiet", help="Does not print to console.",
                                 dest="quiet", action='store_true'),
    argumentsParser.add_argument(
        "-a", "--apikey", help='API key for AlienVaultOTX', dest="api_key")

    return argumentsParser.parse_args()

def isValidData(data):
    if(data == ""):
        return False
    return True

def checkIPForPulses(ip_address, api_key):

    with Progress(transient=True) as ipCheckProgress:
        ipTask = ipCheckProgress.add_task("IP Check:", total=10)

        endpoint = f"https://otx.alienvault.com/api/v1/indicators/IPv4/{ip_address}/general"
        headers = {'X-OTX-API-KEY': f'{api_key}'}
        ipCheckProgress.update(ipTask, advance=2)

        res = requests.get(endpoint, headers=headers)
        ipCheckProgress.update(ipTask, advance=4)

        if(res.status_code == 200):
            ipCheckProgress.update(ipTask, advance=2)

            return res.json()
        else:
            ipCheckProgress.update(ipTask, advance=2)

            return ""

def checkDomainForPulses(domain_name, api_key):

    with Progress(transient=True) as domainCheckProgress:
        domainTask = domainCheckProgress.add_task("Domain Check:", total=10)

        endpoint = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain_name}/general"
        headers = {'X-OTX-API-KEY': f'{api_key}'}
        domainCheckProgress.update(domainTask, advance=2)

        res = requests.get(endpoint, headers=headers)
        domainCheckProgress.update(domainTask, advance=4)

        if(res.status_code == 200):
            domainCheckProgress.update(domainTask, advance=2)

            return res.json()
        else:
            domainCheckProgress.update(domainTask, advance=2)

            return ""

def convertRichToMarkdown(string):

    data = str(string)

    patterns = {
        r'\[bold\]': f'\n**',
        r'\[\/bold\]': '**',
        r'\[bold black on green blink\]': f'\n***',
        r'\[\/bold black on green blink\]': '***',
        r'\[bold italic\]': f'\n## ',
        r'\[\/bold italic\]': '',
        # Converts a link with the contents intact.
        r'\[link=(.*?)\]\1\[\/link\]': fr'\n[\1](\1)',
    }

    for pattern in patterns:
        data = re.sub(pattern, patterns[pattern], data)

    return data

def parsePulseResponse(data, arg):

    pulse_info = data['pulse_info']

    malware_families = []
    output = []

    divider = f"\n----"

    fPulseHeader = f"[bold italic]Pulse Information for {arg}[/bold italic]"

    fCount = "[bold]Count[/bold]"
    count = pulse_info['count']

    output.append(fPulseHeader)
    output.append(fCount)
    output.append(count)

    for pulse in pulse_info['pulses']:
        fPulse = "[bold]Pulse[/bold]"
        pulseName = pulse['name']

        output.append(fPulse)
        output.append(pulseName)

        if(pulse['description']):
            fPulseDescriptionHeader = "[bold]Description[/bold]"
            pulseDescription = pulse['description']

            output.append(fPulseDescriptionHeader)
            output.append(pulseDescription)

        if(pulse['author']):
            fPulseAuthorHeader = "[bold]Author[/bold]"
            pulseAuthor = pulse['author']['username']

            output.append(fPulseAuthorHeader)
            output.append(pulseAuthor)

        output.append(divider)

    fPulseAdditionalDetailsHeader = "[bold italic]Additional Details[/bold italic]"

    output.append(fPulseAdditionalDetailsHeader)

    if(pulse_info['related']):
        for group in pulse_info['related']:

            if(pulse_info['related'][group]['malware_families']):
                fPulseAssociatedMalwareFamiliesHeader = "[bold]Associated Malware families[/bold]"

                output.append(fPulseAssociatedMalwareFamiliesHeader)

                for malware in pulse_info['related'][group]['malware_families']:
                    malware_families.append(malware)

                    fPulseMalware = f"- {malware}"

                    output.append(fPulseMalware)

    if(pulse_info['references']):
        fPulseReferencesHeader = "[bold]References[/bold]"

        output.append(fPulseReferencesHeader)

        for reference in pulse_info['references']:
            fReference = f'[link={reference}]{reference}[/link]'

            output.append(fReference)

    return output

def runPulseCheck(arg):
    if(arg == args.domain):
        data = checkDomainForPulses(args.domain, args.api_key)

    elif(arg == args.ip):
        data = checkIPForPulses(args.ip, args.api_key)

    else:
        data = ""

    rprint("")

    output = parsePulseResponse(data, arg)

    if(isValidData(output) is False):
        response = f'[bold black on red blink]:warning: Failed to get valid response! [/bold black on red blink]'

    else:
        response = f'[bold black on green blink]Successfully retrieved data on {arg}[/bold black on green blink]'

    if(args.quiet is False):
        if(args.markdown):

            rprint(convertRichToMarkdown(response))
            for line in output:
                rprint(convertRichToMarkdown(line))

        else:
            rprint(response)
            for line in output:
                rprint(line)

    return output

def exportResults(data, filename):

    if(args.markdown):

        file = open(filename, 'w')
        for line in data:
            file.write(convertRichToMarkdown(line) + "\n")

        file.close()

# ----------------------------------------------------- #

args = registerArguments()

def main():

    if(args.api_key is None):
        rprint('[bold black on red blink]:warning: No API Key provided! Exiting... [/bold black on red blink]')
        exit()

    if(args.ip is not None):
        rprint(f'Checking IP data for {args.ip}')
        check_data = runPulseCheck(args.ip)
        exportResults(check_data, filename=f'ip_{args.ip}.md')


    if(args.domain is not None):
        rprint(f'Checking domain data for {args.domain}...')
        check_data = runPulseCheck(args.domain)
        exportResults(check_data, filename=f'domain_{args.domain}.md')

    fCompletedPulse = "[bold black on green blink]Enrichment complete.[/bold black on green blink]"
    if(args.quiet is False):
        if(args.markdown):
            rprint(convertRichToMarkdown(fCompletedPulse))
        else:
            rprint(fCompletedPulse)
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
