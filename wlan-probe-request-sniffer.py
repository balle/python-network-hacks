#!/usr/bin/python3

from datetime import datetime
from scapy.all import *

iface = "wlp2s0"
iwconfig_cmd = "/usr/sbin/iwconfig"

# Print ssid and source address of probe requests
def handle_packet(packet):
    if packet.haslayer(Dot11ProbeResp):
        print(str(datetime.now()) + " " + packet[Dot11].addr2 + \
        " searches for " + packet.info)

# Set device into monitor mode
os.system(iwconfig_cmd + " " + iface + " mode monitor")

# Start sniffing
print("Sniffing on interface " + iface)
sniff(iface=iface, prn=handle_packet)
