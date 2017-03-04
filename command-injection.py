#!/usr/bin/python

###[ Loading modules

import sys
import httplib2
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup


###[ Global vars

max_urls = 999
inject_chars = ["|",
                "&&",
                ";",
                '`']
error_msgs = [
    "syntax error",
    "command not found",
    "permission denied",
]

# ...