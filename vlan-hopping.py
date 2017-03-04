#!/usr/bin/python

from scapy.all import *

packet = Ether(dst="c0:d3:de:ad:be:ef") / \
         Dot1Q(vlan=1) / \
         Dot1Q(vlan=2) / \
         IP(dst="192.168.13.3") / \
         ICMP()

sendp(packet)
