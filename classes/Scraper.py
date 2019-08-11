#!/usr/bin/env python3

from __future__ import print_function
from __future__ import absolute_import

## Standard Libraries
import os
import sys
import re
from pprint import pprint,pformat

## Third-Party
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

## Modules
from .BuildingBlocks import State               #pylint: disable=relative-beyond-top-level
from .BuildingBlocks import BaseObject          #pylint: disable=relative-beyond-top-level
from .WorkFunctions import extractCount         #pylint: disable=relative-beyond-top-level
from .WorkFunctions import getLinks             #pylint: disable=relative-beyond-top-level
from .WorkFunctions import getFileName          #pylint: disable=relative-beyond-top-level
from .WorkFunctions import writeUrlToDisk       #pylint: disable=relative-beyond-top-level

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
    
    def doHEADRequest(self, url):
        try:
            resp = self.lastRequestResponse = self.req.head(url)
            resp.raise_for_status()
            return resp
        except:
            raise

    def doGETRequest(self, url):
        try:
            resp = self.lastRequestResponse = self.req.get(url)
            resp.raise_for_status()
            return resp
        except:
            raise
        
    def doGETStream(self, url):
        try:
            resp = self.lastRequestResponse = self.req.get(url, stream=True)
            resp.raise_for_status()
            return resp
        except:
            raise

class YPScraper(Scraper):

    def __init__(self, base_url="https://yiff.party", matchers=["patreon_data", "patreon_inline"]):
        self.base_url = base_url
        self.href_matchers = matchers

    def getBaseUrl(self):
        return self.base_url

    def loadPatreonID(self, pid):
        url = self.lastUrl = urljoin(self.base_url, str(pid))
        self.lastResponse = self.doGETRequest(url)
        return self.lastResponse        

    def patreonMetadata(self, pid):
        resp = self.loadPatreonID(pid)
        soup = self.soup = BeautifulSoup(resp.content, "html.parser")
        artist = soup.find_all('span', {"class": "yp-info-name"})[0].string
        counts_containers = soup.find_all('li', {"class": "tab col s6"})
        for item in counts_containers:
            if "Patreon" in item.string:
                patreon_post_count = extractCount(item.string)
            elif "Shared" in item.string:
                shared_file_count = extractCount(item.string)
        patreon_links, other_links = getLinks(self.soup, self.href_matchers)
        return {
            'artist': artist,
            'patreon_post_count': patreon_post_count,
            'shared_file_count': shared_file_count,
            'patreon_links': patreon_links,
            'other_links': other_links,
        }

        
def main():
    pass

if __name__=="__main__":
    main()
