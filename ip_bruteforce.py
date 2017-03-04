#!/usr/bin/python2

import os
import re
import sys
from random import randint

device = "wlan0"
ips = range(1,254)

def ping_ip(ip):
	fh = os.popen("ping -c 1 -W 1 " + ip)
	resp = fh.read()

	if re.search("bytes from", resp, re.MULTILINE):
		print "Got response from " + ip
		sys.exit(0)

while len(ips) > 0:
	host_byte = randint(2, 253)
	idx = randint(0, len(ips) - 1)
	ip = ips[idx]
	del ips[idx]

	print "Checking net 192.168." + str(ip) + ".0"
        cmd = "ifconfig " + device + " 192.168." + str(ip) + \
              "." + str(host_byte) + " up"
	os.system(cmd)
	ping_ip("192.168." + str(ip) + ".1")
	ping_ip("192.168." + str(ip) + ".254")
