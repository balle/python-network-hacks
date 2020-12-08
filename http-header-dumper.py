#!/usr/bin/python3

import sys
import requests

if len(sys.argv) < 2:
    print(sys.argv[0] + ": <url>")
    sys.exit(1)

r = requests.get(sys.argv[1])

for field, value in r.headers.items():
    print(field + ": " + value)
