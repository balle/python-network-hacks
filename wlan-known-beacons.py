#!/usr/bin/python3

import os
import sys
import time
from scapy.all import *

iface = "wlp2s0"
iwconfig_cmd = "/usr/sbin/iwconfig"
mymac = "aa:bb:cc:aa:bb:cc"
interval = 1


def send_beacon(ssid):
    pkt = RadioTap() / \
          Dot11(addr1='ff:ff:ff:ff:ff:ff',
                addr2=mymac, addr3=mymac) / \
          Dot11Beacon() / \
          Dot11Elt(ID='SSID', info=ssid, len=len(ssid))
    
    print("Sending beacon for SSID " + ssid)
    sendp(pkt, iface=iface)


if len(sys.argv) < 2:
    print(sys.argv[0] + " <dict_file>")
    sys.exit

# Set card in access point mode
os.system(iwconfig_cmd + " " + iface + " mode master")

dict = []

with open(sys.argv[1]) as fh:
    dict = fh.readlines()
    
while 1:
    for ssid in dict:
        send_beacon(ssid)

    time.sleep(interval)
