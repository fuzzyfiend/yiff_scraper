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

# Modules
from classes.BuildingBlocks import State 
from classes.ErrorFunctions import handleBacktrace

def preinit():
    ## import program state
    pg_state = State()

    #region BuildArgParser
    parser = argparse.ArgumentParser(description=__code_desc__)
    parser.add_argument('-V','--version', action='version', version='%(prog)s '+__code_version__)
    parser.add_argument('-v','--verbose', action='count', default=0, help="Print verbose output to the console. Multiple v's increase verbosity")
    parser.add_argument('--debug', action='store_true', help="Toggle debugging output to the console.")
    args = parser.parse_args()
    pg_state.args = args
    #endregion

def init():
    pg_state = State()
    args = pg_state.args
    ## Do program-specific initialization here

def main():
    ## PreInit program state and handle arguments
    preinit()
    pg_state = State()
    args = pg_state.args
 
    ## Begin program execution with support for verbose/debuging
    try:
        init()

    except Exception as e:
        if args.debug:
            print("[<>] Caught Exception for handling")
            print("[<>] Cloning Stack")
            stack = deepcopy(locals())
            handleBacktrace(stack)
        else:
            raise

if __name__=="__main__":
    main()
