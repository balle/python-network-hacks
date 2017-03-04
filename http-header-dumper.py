#!/usr/bin/python

import sys
import httplib2

if len(sys.argv) < 2:
    print sys.argv[0] + ": <url>"
    sys.exit(1)

webclient = httplib2.Http()
header, content = webclient.request(sys.argv[1], "GET")

for field, value in header.items():
    print field + ": " + value
