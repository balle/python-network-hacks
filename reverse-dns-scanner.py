#!/usr/bin/python3

import sys
import socket
from random import randint

if len(sys.argv) < 2:
    print(sys.argv[0] + ": <start_ip>-<stop_ip>")
    sys.exit(1)


def get_ips(start_ip, stop_ip):
    ips = []
    tmp = []

    for i in start_ip.split('.'):
        tmp.append("%02X" % int(i))

    start_dec = int(''.join(tmp), 16)
    tmp = []

    for i in stop_ip.split('.'):
        tmp.append("%02X" % int(i))

    stop_dec = int(''.join(tmp), 16)

    while(start_dec < stop_dec + 1):
        bytes = []
        bytes.append(str(int(start_dec / 16777216)))
        rem = start_dec % 16777216
        bytes.append(str(int(rem / 65536)))
        rem = rem % 65536
        bytes.append(str(int(rem / 256)))
        rem = rem % 256
        bytes.append(str(rem))
        ips.append(".".join(bytes))
        start_dec += 1

    return ips


def dns_reverse_lookup(start_ip, stop_ip):
    ips = get_ips(start_ip, stop_ip)

    while len(ips) > 0:
        i = randint(0, len(ips) - 1)
        lookup_ip = str(ips[i])
        resolved_name = None
        
        try:
            resolved_name = socket.gethostbyaddr(lookup_ip)[0]
        except socket.herror as e:
            # Ignore unknown hosts
            pass
        except socket.error as e:
            print(str(e))

        if resolved_name:
            print(lookup_ip + ":\t" + resolved_name)
            
        del ips[i]

start_ip, stop_ip = sys.argv[1].split('-')
dns_reverse_lookup(start_ip, stop_ip)
