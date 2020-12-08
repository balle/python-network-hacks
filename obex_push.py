#!/usr/bin/python3

import sys
from os.path import basename
from PyOBEX import client, headers, responses


if len(sys.argv) < 4:
    print(sys.argv[0] + ": <btaddr> <channel> <file>")
    sys.exit(0)

btaddr = sys.argv[1]
channel = int(sys.argv[2])
my_file = sys.argv[3]

c = client.Client(btaddr, channel)
r = None

try:
    print("Connecting to %s on channel %d" % (btaddr, channel))
    r = c.connect(header_list=(headers.Target("OBEXObjectPush"),))
except OSError as e:
    print("Connect failed. " + str(e))
    
if isinstance(r, responses.ConnectSuccess):
    print("Uploading file " + my_file)
    r = c.put(basename(my_file), open(my_file, "rb").read())

    if not isinstance(r, responses.Success):
        print("Failed!")
        
    c.disconnect()
    
else:
    print("Connect failed!")
    
