#!/usr/bin/python3

from scapy.all import *

iface = "wlp2s0"
iwconfig_cmd = "/usr/sbin/iwconfig"

wpa_handshake = []

def handle_packet(packet):
    # Got EAPOL KEY packet
    if packet.haslayer(EAPOL) and packet.type == 2:
        print(packet.summary())
        wpa_handshake.append(packet)

        # Got complete handshake? Dump it to pcap file
        if len(wpa_handshake) >= 4:
            wrpcap("wpa_handshake.pcap", wpa_handshake)


# Set device into monitor mode
os.system(iwconfig_cmd + " " + iface + " mode monitor")

# Start sniffing
print("Sniffing on interface " + iface)
sniff(iface=iface, prn=handle_packet)
