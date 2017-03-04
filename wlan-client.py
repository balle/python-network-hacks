#!/usr/bin/python

from scapy.all import *


station = "d0:01:5f:1e:21:f3"
ssid = "LoveMe"
iface = "wlan0"

# probe request
pkt = RadioTap() / \
    Dot11(addr1='ff:ff:ff:ff:ff:ff',
          addr2=station, addr3=station) / \
    Dot11ProbeReq() / \
    Dot11Elt(ID='SSID', info=ssid, len=len(ssid))
print "Sending probe request"
res = srp1(pkt, iface=iface)
bssid = res.addr2
print "Got answer from " + bssid

# authentication with open system
pkt = RadioTap() / \
    Dot11(subtype=0xb,
          addr1=bssid, addr2=station, addr3=bssid) / \
    Dot11Auth(algo=0, seqnum=1, status=0)
print "Sending authentication"
res = srp1(pkt, iface=iface)
res.summary()

# association
pkt = RadioTap() / \
    Dot11(addr1=bssid, addr2=station, addr3=bssid) / \
    Dot11AssoReq() / \
    Dot11Elt(ID='SSID', info=ssid) / \
    Dot11Elt(ID="Rates", info="\x82\x84\x0b\x16")

print "Association request"
res = srp1(pkt, iface=iface)
res.summary()
