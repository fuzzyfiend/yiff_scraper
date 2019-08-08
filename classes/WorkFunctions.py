#!/usr/bin/env python3

from __future__ import print_function
from __future__ import absolute_import

import re

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
