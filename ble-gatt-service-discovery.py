#!/usr/bin/python3

from gattlib import GATTRequester
import sys

if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " <addr>")
    sys.exit(0)

req = GATTRequester(sys.argv[1], True)

for service in requester.discover_primary():
    print(service)
