#!/usr/bin/python

import bluetooth
import sys

if len(sys.argv) < 2:
    print "Usage: " + sys.argv[0] + " <addr>"
    sys.exit(0)

services = bluetooth.find_service(address=sys.argv[1])

if(len(services) < 1):
    print "No services found"
else:
    for service in services:
        for (key, value) in service.items():
            print key + ": " + str(value)
        print ""
