#!/usr/bin/python3

import sys
import socket

if len(sys.argv) < 3:
    print(sys.argv[0] + ": <dict_file> <domain>")
    sys.exit(1)


def do_dns_lookup(name):
    try:
        print(name + ": " + socket.gethostbyname(name))
    except socket.gaierror as e:
        print(name + ": " + str(e))

try:
    fh = open(sys.argv[1], "r")

    for word in fh.readlines():
        subdomain = word.strip()

        if subdomain:
            do_dns_lookup(word.strip() + "." + sys.argv[2])

    fh.close()
except IOError:
    print("Cannot read dictionary " + file)
