#!/usr/bin/python3

import sys
import requests

if len(sys.argv) < 3:
    print(sys.argv[0] + ": <url> <key> <value>")
    sys.exit(1)

headers = {'Cookie': sys.argv[2] + '=' + sys.argv[3]}
r = requests.get(sys.argv[1], data=headers)

print(r.content)
