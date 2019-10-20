#!/usr/bin/env python3

from __future__ import print_function
from __future__ import absolute_import

## Standard Libraries
import os
import sys
import time
from pprint import pprint

## Third-Party
import requests
from requests import HTTPError,ConnectionError,Timeout,RequestException
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

## Modules
from .BuildingBlocks import BaseObject          #pylint: disable=relative-beyond-top-level
from .BuildingBlocks import State               #pylint: disable=relative-beyond-top-level

class Scraper(BaseObject):

    def __init__(self):
        self.supported_methods = [
            "HEAD",
            "GET",
        ]
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
        o = State()
        super().__init__(state=o)
        self.args = o.args              #pylint: disable=no-member
        self.diskcache = o.diskcache    #pylint: disable=no-member
        self.req = self.Session()
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

    #https://www.peterbe.com/plog/best-practice-with-retries-with-requests
    def Session(self, retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):
        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def doRequest(self, method, url, params=None, stream=False):
        if method not in self.supported_methods:
            raise ValueError("(%s) not in (%s)" % (method, self.supported_methods))

        try:
            if params == None:
                resp = self.lastRequestResponse = self.req.request(method=method, url=url, stream=stream)
            else:
                resp = self.lastRequestResponse = self.req.request(method=method, url=url, params=params, stream=stream)
            resp.raise_for_status()
            return resp
        except Timeout as e:
            pprint(e)
            raise
        except ConnectionError as e:
            pprint(e)
            raise
        except HTTPError as e:
            if e.response.status_code == 404:
                #Sometimes we get 404 from yiff.party, can't do anything about it
                print("[!] Caught %d for url (%s); ignoring" %(e.response.status_code, e.response.url))
                return None
            elif e.response.status_code == 504:
                #Gateway timeout; sleep for a bit 
                s=15
                print("[!] Caught %d for url (%s); snoozing for %d seconds" %(e.response.status_code, e.response.url, s))
                time.sleep(s)
                return None
            else:
                raise
        except RequestException as e:
            pprint(e)
            raise
        except Exception as e:
            pprint(e)
            raise

    def doHEADRequest(self, url):
        return self.doRequest(method='HEAD', url=url)

    def doGETRequest(self, url):
        return self.doRequest(method='GET', url=url)

    def doGETRequestWithParams(self, url, params):
        return self.doRequest(method='GET', url=url, params=params)

    def doGETStream(self, url):
        return self.doRequest(method='GET', url=url, stream=True)

def main():
    pass

if __name__=="__main__":
    main()
