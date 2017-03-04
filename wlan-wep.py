#!/usr/bin/python

import sys
from scapy.all import *

iface = "wlan0"
nr_of_wep_packets = 40000
packets = []

# This function will be called for every sniffed packet
def handle_packet(packet):

    # Got WEP packet?
    if packet.haslayer(Dot11WEP):
        packets.append(packet)

        print "Paket " + str(len(packets)) + ": " + \
              packet[Dot11].addr2 + " IV: " + str(packet.iv) + \
              " Keyid: " + str(packet.keyid) + \
              " ICV: " + str(packet.icv)

        # Got enough packets to crack wep key?
        # Save them to pcap file and exit
        if len(packets) == nr_of_wep_packets:
            wrpcap("wpa_handshake.pcap", wpa_handshake)
            sys.exit(0)

# Set device into monitor mode
os.system("iwconfig " + iface + " mode monitor")

# Start sniffing
print "Sniffing on interface " + iface
sniff(iface=iface, prn=handle_packet)
