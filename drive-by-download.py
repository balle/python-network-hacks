#!/usr/bin/python3

from mitmproxy import http
from bs4 import BeautifulSoup

MY_IMAGE_FILE = 'https://www.mydomain.tld/some_image.jpg'

def response(flow: http.HTTPFlow) -> None:
    if flow.response.headers.get("Content-Type") and \
       "text/html" in flow.response.headers["Content-Type"]:
        soup = BeautifulSoup(flow.response.content,
                             features="html.parser")

        for img in soup('img'):
            img['src'] = MY_IMAGE_FILE
    
        flow.response.text = soup.prettify()
    
