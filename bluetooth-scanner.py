#!/usr/bin/python3

import bluetooth as bt

for (addr, name) in bt.discover_devices(lookup_names=True):
    print("%s %s" % (addr, name))

