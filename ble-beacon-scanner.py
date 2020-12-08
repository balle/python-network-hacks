#!/usr/bin/python3

from bluetooth.ble import BeaconService

service = BeaconService()
devices = service.scan(10)

for addr, data in devices.items():
    print("%s (UUID %s Major %d Minor %d Power %d RSSI %d)" % (addr,
                                                               data[0],
                                                               data[1],
                                                               data[2],
                                                               data[3],
                                                               data[4]))

