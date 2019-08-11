#!/usr/bin/env python3

from __future__ import print_function
from __future__ import absolute_import

## Standard Libraries
import os
import sys
from pprint import pprint,pformat

## Third-Party
import requests

## Modules
from .BuildingBlocks import State               #pylint: disable=relative-beyond-top-level
from .BuildingBlocks import BaseObject          #pylint: disable=relative-beyond-top-level

class Scraper(BaseObject):

    def __init__(self):
        self.supported_useragents = [
            # Chrome/Win10
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
            # Firefox/Win10
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0",
            # Safari/OSX
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15",
        ]
        self.supported_accept_headers = [
            # Chrome/Win10
            "accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
        ]
        self.req = requests.Session()
        self.setDefaultHeaders()

    def getTopUserAgent(self):
        return self.supported_useragents[0]

    def getTopAcceptHeader(self):
        return self.supported_accept_headers[0]
        
    def setDefaultHeaders(self):
        self.req.headers.update({
            'User-Agent': self.getTopUserAgent(),
            'Accept': self.getTopUserAgent(),
        })

    def doGETRequest(self, url):
        try:
            resp = self.lastRequestResponse = self.req.get(url)
            resp.raise_for_status()
            return resp
        except:
            raise
        
        
def main():
    pass

if __name__=="__main__":
    main()
