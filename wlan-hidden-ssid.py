#!/usr/bin/python

from scapy.all import *

iface = "wlan0"

# Print ssid of probe requests, probe response 
# or association request
def handle_packet(packet):
    if packet.haslayer(Dot11ProbeReq) or \
	packet.haslayer(Dot11ProbeResp) or \
	packet.haslayer(Dot11AssoReq):
        print "Found SSID " + packet.info

# Set device into monitor mode
os.system("iwconfig " + iface + " mode monitor")

# Start sniffing
print "Sniffing on interface " + iface
sniff(iface=iface, prn=handle_packet)
