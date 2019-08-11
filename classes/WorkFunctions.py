#!/usr/bin/env python3

from __future__ import print_function
from __future__ import absolute_import

import re

## Modules
from .BuildingBlocks import State               #pylint: disable=relative-beyond-top-level

def getFileName(url):
    lst = url.rsplit('/')
    name = lst[-1]
    return name

def extractCount(string):
    match = re.search(r'\d+', string)
    return match.group()

def getLinks(soup, matchers):
    links = soup.find_all('a')
    patreon_links = []
    other_links = []
    for link in links:
        href = link.get('href')
        if href is None:
            continue
        for string in matchers:
            if string not in href:
                other_links.append(href)
            else:
                patreon_links.append(href)
                break
    return list(set(patreon_links)), list(set(other_links))

def writeUrlToDisk(url="", filename=""):
    pg_state = State()
    rs = pg_state.scraper #pylint: disable=no-member
    print("Writing (%s) to: %s" % str(url), str(filename) )
    fp = open(filename, 'wb')
    httpstream = rs.doGETStream(url)
    for chunk in httpstream.iter_content(chunk_size=8192):
        fp.write(chunk)
    fp.close()
    print("Closing: %s" % str(filename))

