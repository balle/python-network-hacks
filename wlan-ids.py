#!/usr/bin/python

import time
from scapy.all import *

iface = "wlan0"

# Nr of max probe responses with different ssids from one addr
max_ssids_per_addr = 5
probe_resp = {}

# Nr of max deauths in timespan seconds
nr_of_max_deauth = 10
deauth_timespan = 23
deauths = {}

# Detect deauth flood and ssid spoofing
def handle_packet(pkt):
    # Got deauth packet
    if pkt.haslayer(Dot11Deauth):
	deauths.setdefault(pkt.addr2, []).append(time.time())
        span = deauths[pkt.addr2][-1] - deauths[pkt.addr2][0]

        # Detected enough deauths? Check the timespan
        if len(deauths[pkt.addr2]) == nr_of_max_deauth and \
           span <= deauth_timespan:
            print "Detected deauth flood from: " + pkt.addr2
            del deauths[pkt.addr2]

    # Got probe response
    elif pkt.haslayer(Dot11ProbeResp):
	probe_resp.setdefault(pkt.addr2, set()).add(pkt.info)

        # Detected too much ssids from one addr?
        if len(probe_resp[pkt.addr2]) == max_ssids_per_addr:
            print "Detected ssid spoofing from " + pkt.addr2

            for ssid in probe_resp[pkt.addr2]:
                print ssid

            print ""
            del probe_resp[pkt.addr2]


# Parse parameter
if len(sys.argv) > 1:
    iface = sys.argv[1]

# Set device into monitor mode
os.system("iwconfig " + iface + " mode monitor")

# Start sniffing
print "Sniffing on interface " + iface
sniff(iface=iface, prn=handle_packet)
