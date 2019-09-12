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
import json
from pprint import pprint, pformat

# Third-Party Libraries
from diskcache import Cache

# Modules
from classes.BuildingBlocks import State
from classes.YiffScraper import YPScraper
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
    parser.add_argument('-c', '--config', default="config.json", help="A JSON configuration to load. Default is '%(default)s'")
    parser.add_argument('--caching-dir', default=".ypcache", help="Directory for caching metadata. Default is '%(default)s'")
    parser.add_argument('--flush-cache', action='store_true', help="Toggle to flush the cache prior to running")
    pg_state.args = parser.parse_args()
    #endregion

def init():
    pg_state = State()
    args = pg_state.args

    pg_state.exec_file = os.path.basename(__file__)
    pg_state.exec_dir = os.path.dirname(__file__)
    pg_state.exec_fpath = os.path.abspath(__file__)
    pg_state.output_dir = os.path.join(pg_state.exec_dir, args.output)
    if args.verbose > 1:
        crit = ["exec_file", "exec_dir", "exec_fpath", "output_dir"]
        vLogPGVars(crit, pg_state)
    os.chdir(pg_state.exec_dir)

    if args.config:
        print("[*] Loading configuration file: %s" % args.config)
        j = pg_state.config = json.load(open(args.config))
        pg_state.patreon_dict = j["patreon"]

    pg_state.diskcache = Cache(directory=args.caching_dir)
    if args.flush_cache:
        pg_state.diskcache.clear()
    pg_state.scraper = YPScraper()
        
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
        if args.verbose:
            print('[*] set pg_state.output_path = %s' % (pg_state.output_path) )
            print('[*] --> This directory will be created if absent and navigated into')

        #[55578,2479000,96435,9608858,706437,126683,881792,175584,460110,777164,3571295,253549,106008,10404964,690415,215736,3708137,2285596,121401,16943278,140212,2937211,10329385,7216191]
        #patreon_list = pg_state.patreon_list = [55578,2479000,96435,9608858,706437,126683,881792,175584,460110,777164,3571295,253549,106008,10404964,690415,215736,3708137,2285596,121401,16943278,140212,2937211,10329385,7216191]

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
