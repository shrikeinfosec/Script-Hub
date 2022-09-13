## Description

A  utility script to extract links matching social media pages from the provided link/file.

*This requires the [geckodriver](https://github.com/mozilla/geckodriver/releases) webdriver to be installed in your PATH.*

## Installation

1. Download the script (either by cloning the repo or downloading the individual `social_extractor.py` and `requirements.txt` files).
2. Run `python -m pip install -r requirements.txt`
3. Run `python social_extractor.py` with one of the examples below (as a reference).

## Examples

Extract links from one url:

`$ python social_extractor.py -l https://twitch.tv/ashen/about`

Extract links from a file of urls:

`$ python social_extractor.py -f links.txt`

## Todo
- Implement better formatting in console.
- Add support for exporting links to a file (txt or csv).