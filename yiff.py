#!/usr/bin/env python3

# Future Declarations
from __future__ import print_function
from __future__ import absolute_import

# Dunders
__code_version__ = 'v0.0.1'
__code_desc__ = """
Scrape yiff.party for archival purposes
    ex: python3 {name}
""".format(name=__file__)

# Standard Libraries
import os
import sys
import argparse
from pprint import pprint, pformat
from copy import deepcopy as deepcopy

# Third-Party Libraries
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Modules
from classes.BuildingBlocks import State
from classes.Scraper import Scraper
from classes.WorkFunctions import extractCount
from classes.WorkFunctions import getLinks
from classes.ErrorFunctions import vLogPGVars
from classes.ErrorFunctions import handleBacktrace


def preinit():
    ## import program state
    pg_state = State()

    #region BuildArgParser
    parser = argparse.ArgumentParser(description=__code_desc__)
    parser.add_argument('-V', '--version', action='version', version='%(prog)s '+__code_version__)
    parser.add_argument('-v', '--verbose', action='count', default=0, help="Print verbose output to the console. Multiple v's increase verbosity")
    parser.add_argument('--debug', action='store_true', help="Toggle debugging output to the console.")
    parser.add_argument('-o', '--output', default='siterip', help="Write all files and directory structure to the following location. Default is '%(default)s'")
    pg_state.args = parser.parse_args()
    #endregion

def init():
    pg_state = State()
    args = pg_state.args
    pg_state.exec_file = os.path.basename(__file__)
    pg_state.exec_dir = os.path.dirname(__file__)
    pg_state.exec_fpath = os.path.abspath(__file__)
    pg_state.output_dir = os.path.join(pg_state.exec_dir, args.output)
def main():
    ## PreInit program state and handle arguments
    preinit()
    pg_state = State()
    args = pg_state.args

    ## Begin program execution with support for verbose/debuging
    try:
        init()

        # Create directories and chdir
        output_path = pg_state.output_path = os.path.abspath(pg_state.output_dir)        
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        os.chdir(output_path)

        # define basic vars
        base_url = pg_state.base_url = 'https://yiff.party'
        matchers = pg_state.matchers = ["patreon_data", "patreon_inline"]        
        # use the following for testing purposes
        # 20645128 has relatively few submissions
        # 881729 has quite a few submissions and saved files that span multiple pages
        patrons_list = pg_state.patrons_list = [20645128, 881792]
        for pid in patrons_list:
            url = pg_state.lastUrl = urljoin(base_url, str(pid))
            response = pg_state.lastRequestsResponse = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            artist = soup.find_all('span', {"class": "yp-info-name"})[0].string
            counts_containers = soup.find_all('li', {"class": "tab col s6"})
            for item in counts_containers:
                if "Patreon" in item.string:
                    patreon_post_count = extractCount(item.string)
                elif "Shared" in item.string:
                    shared_file_count = extractCount(item.string)


            # create artist directory and/or chdir to it
            target = pg_state.lastTarget = os.path.join(output_path, artist)
            if not os.path.exists(target):
                os.makedirs(target)
            os.chdir(target)

            patreon_links, other_links = getLinks(soup, matchers)
            for link in patreon_links:
                url = pg_state.lastUrl = urljoin(base_url, str(link))
     
    except Exception as e:
        if args.debug:
            print("[<>] Caught Exception for handling")
            print("[<>] Cloning Stack")
            #stack = deepcopy(locals())
            stack = locals()
            handleBacktrace(stack)
        else:
            raise

if __name__=="__main__":
    main()
