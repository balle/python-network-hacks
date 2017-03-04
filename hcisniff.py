#!/usr/bin/python

import sys
import struct
import bluetooth._bluetooth as bt

# Open hci socket
sock = bt.hci_open_dev(0)

# Get data direction information
sock.setsockopt(bt.SOL_HCI, bt.HCI_DATA_DIR, 1)

# Get timestamps
sock.setsockopt(bt.SOL_HCI, bt.HCI_TIME_STAMP, 1)

# Construct and set filter to sniff all hci events
# and all packet types
filter = bt.hci_filter_new()
bt.hci_filter_all_events(filter)
bt.hci_filter_all_ptypes(filter)
sock.setsockopt(bt.SOL_HCI, bt.HCI_FILTER, filter)

# Start sniffing
while True:
    # Read first 3 byte
    header = sock.recv(3)

    if header:
        # Decode them and read the rest of the packet
        ptype, event, plen = struct.unpack("BBB", header)
        packet = sock.recv(plen)

        print "Ptype: " + str(ptype) + " Event: " + str(event)
        print "Packet: "

        # Got ACL data connection? Try to dump it in ascii
        # otherwise dump the packet in hex
        if ptype == bt.HCI_ACLDATA_PKT:
            print packet + "\n"
        else:
            for c in packet:
                hex = struct.unpack("B",c)[0]
                sys.stdout.write("%02x " % hex)
            print "\n"

    # Got no data
    else:
        break

sock.close()