#!/usr/bin/python3

from bluetooth.ble import DiscoveryService

service = DiscoveryService()
devices = service.discover(2)

for addr, name in devices.items():
    print("Found %s (%s)" % (name, addr))

