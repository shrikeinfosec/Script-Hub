## Description

A utility script to check ip/domains for AlienVault OTX Pulses.

An API key *MUST* be provided - you can register for one at https://otx.alienvault.com/api and signing-up for an account.

## Installation

1. Download the script (either by cloning the repo or downloading the individual `otx_lookup.py` and `requirements.txt` files).
2. Run `python -m pip install -r requirements.txt`
3. Run `python otx_lookup.py` with one of the examples below (as a reference).

## Examples

Look up a single IP:

`$ python otx_lookup.py -i 1.1.1.1 -a <API_KEY>`

Look up a single IP without printing to the console:

`$ python otx_lookup.py -i 1.1.1.1 -a <API_KEY> -q`
    
Lookup a domain:

`$ python otx_lookup.py -d google.com -a <API_KEY>`
    
Lookup a domain and export the results to a .md file:

`$ python otx_lookup.py -d google.com -a <API_KEY> -m`

(*In future, this will support an optional -f flag for a filename to be specified.*)
    
## Todo
- Implement the `-f` argument to specify a filename for an exported markdown file.
- Add support for multiple IP addresses or domains read from a text file.
