#!/usr/bin/python3

###[ Loading modules

import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


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
