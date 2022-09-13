#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" social_extractor.py: A utility script to extract links matching social
     media pages from the provided link/file."""

# Ownership, licensing and usage documentation
# can be found at the bottom of this script.

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from argparse import ArgumentParser
from tldextract import extract
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import sys

# ----------------------------------------------------- #

start_url = ""
file = ""
supported_domains = ["twitch.tv", "twitter.com", "instagram.com", "tiktok.com", "youtube.com", "fanhouse.app"]
ignored_pages = ["tos", "privacy", "/products/", "legal"]
options = Options()
options.add_argument('--headless')
browser = webdriver.Firefox(options=options)
parsed_links = []


def register_arguments():
    ''' Registers the arguments for the script.'''
    arguments_parser = ArgumentParser(
        description='Utility script to extract links matching social media pages from the provided link/file.')

    arguments_parser.add_argument(
        "-l", "--link", help='A link to start with', dest="start_url")
    arguments_parser.add_argument(
        "-f", "--file", help='A file containing a number of links.',
        dest="file")
    return arguments_parser.parse_args()


def makeRequest(url):

    print(f"Making request to {url}...")
    # reqs = requests.get(url)
    browser.get(url)
    print("Waiting for page to fully populate...")
    time.sleep(10)
    reqs = browser.page_source
    soup = BeautifulSoup(reqs, 'lxml')
    print(f"Parsing {url} for links")
    # print(soup)

    base_domain, tsu = extractDomainFromLink(url)
    print(f"Base Domain identified as {base_domain}")
    for link in soup.find_all('a'):
        parsed = link.get('href').split('?')[0]
        if any(substring in parsed for substring in ignored_pages) is False:
            if parsed not in parsed_links:
                processLink(parsed)

    for link in soup.find_all('link'):
        parsed = link.get('href').split('?')[0]
        if any(substring in parsed for substring in ignored_pages) is False:
            if parsed not in parsed_links:
                processLink(parsed)


def extractDomainFromLink(link):
    tsd, td, tsu = extract(link)
    domain = f"{td}.{tsu}"
    return domain, tsd


def processLink(link):
    domain, tsd = extractDomainFromLink(link)
    if domain in supported_domains and (tsd == "" or tsd == "www"):
        print(f"Valid link: {link}")
        parsed_links.append(link)


# ----------------------------------------------------- #


args = register_arguments()


def main():
    if args.start_url is None and args.file is None:
        print("You have not specified a target URL.")
        sys.exit()
    if args.start_url is not None and args.file is not None:
        print("You have specified a link and a file - please only use \
             one argument.")
        sys.exit()
    if args.start_url is not None:
        makeRequest(args.start_url)
    if args.file is not None:
        file = open(args.file)
        for line in file:
            print(f"Extracting links from {line}")
            makeRequest(line)


if __name__ == "__main__":
    main()
    browser.quit()

# ------------------------------------------------- #

"""
@Author = "Shrike InfoSec"
@Licence = "MIT"
@Version = "1.0.0"
@Email = "shrike@shrikeinfosec.org"
@Status = "In Development"
"""

"""
    This project requires the use of the Firefox geckodriver for selenium.
    It will need to be installed in your PATH for this script to work.

Examples:
    Extract links from one url:
        $ python social_extractor.py -l https://twitch.tv/ashen/about
    Extract links from a file of urls:
        $ python social_extractor.py -f links.txt
Todo:
    * Implement better formatting in console.
    * Add support for exporting links to a file (txt or csv).
"""
