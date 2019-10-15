#!/usr/bin/env python3

from __future__ import print_function
from __future__ import absolute_import

## Standard Libraries
import os
import sys
import re
from copy import deepcopy
from pprint import pprint

## Third-Party
from urllib.parse import urljoin
from bs4 import BeautifulSoup

## Modules
from .Scraper import Scraper                    #pylint: disable=relative-beyond-top-level
from .WorkFunctions import getAllLinks          #pylint: disable=relative-beyond-top-level

class YPScraper(Scraper):

    def __init__(self, base_url="https://yiff.party", matchers=["patreon_data", "patreon_inline"]):
        super().__init__()
        self.base_url = base_url
        self.href_matchers = matchers

    def getBaseUrl(self):
        return self.base_url

    def loadPatreonID(self, pid):
        url = self.lastUrl = urljoin(self.base_url, str(pid))
        if self.tracking_state:
            if self.pg_state.args.verbose:
                print("[**] GET URL: (%s)" % (url))
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
        print('[+] Determined artist: %s' % artist)
        print('[+] Determined patreon_post_count: %d' % int(patreon_post_count))
        print('[+] Determined shared_file_count: %d' % int(shared_file_count))

        return {
            'artist': artist,
            'patreon_post_count': patreon_post_count,
            'shared_file_count': shared_file_count,
            'patreon_links': patreon_links,
            'other_links': other_links,
        }

    """ Called on cache misses or cache invalid """    
    def cacheEntry(self, target):
        url = self.lastUrl = urljoin(self.base_url, str(target))
        resp_headers = self.doHEADRequest(url).headers
        headers = dict(deepcopy(resp_headers))
        uselessHeaders = [ 'Age', 'Server', 'Expect-CT', 'CF-RAY', 'CF-Cache-Status',
            'X-Content-Type-Options', 'Strict-Transport-Security'
        ]
        # remove extraneous headers to reduce cache size.
        headers = self.deleteHeaders(headers, uselessHeaders)
        # extract etag as caching key, extract expire time in sec by Cache-Control
        try:
            etag = headers['ETag']
            expire = 604800 # 7 days by default
            cc = headers['Cache-Control'].split(',')
            for el in cc:
                if 'max-age' in el:
                    expire = el.split('=')[1]
            self.diskcache.set(etag, headers, expire=int(expire))
            self.diskcache.set(url, etag, expire=int(expire))
            return headers
        except KeyError:
            return headers


def main():
    pass

if __name__=="__main__":
    main()
