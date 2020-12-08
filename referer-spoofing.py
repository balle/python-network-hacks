#!/usr/bin/python3

import sys
import requests

if len(sys.argv) < 2:
    print(sys.argv[0] + ": <url>")
    sys.exit(1)

headers = {'Referer': 'http://www.peter-lustig.com'}
r = requests.get(sys.argv[1], data=headers)

print(r.content)
