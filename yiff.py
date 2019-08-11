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

# Third-Party Libraries

# Modules
from classes.BuildingBlocks import State
from classes.Scraper import YPScraper
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

    pg_state.scraper = YPScraper()
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
        rs = pg_state.scraper

        # Create directories and chdir
        output_path = pg_state.output_path = os.path.abspath(pg_state.output_dir)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        os.chdir(output_path)

        # use the following for testing purposes
        # 20645128 has relatively few submissions
        # 881729 has quite a few submissions and saved files that span multiple pages
        patreon_list = pg_state.patreon_list = [20645128, 881792]

        # foreach patreon
        for pid in patreon_list:
            metadata = pg_state.patreon_metadata = rs.patreonMetadata(pid)
            artist = metadata['artist']
            patreon_links = metadata['patreon_links']


            # create artist directory and/or chdir to it
            target = pg_state.lastTarget = os.path.join(output_path, artist)
            if not os.path.exists(target):
                os.makedirs(target)
            os.chdir(target)
                
            for link in patreon_links:
                rs.download(link)

    except Exception as e:
        if args.debug:
            print("[<>] Caught Exception for handling")
            print("[<>] Cloning Stack")
            stack = locals()
            handleBacktrace(stack)
        else:
            raise

if __name__=="__main__":
    main()
