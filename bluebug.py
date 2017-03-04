#!/usr/bin/python

import sys
import lightblue

if len(sys.argv) < 2:
    print sys.argv[0] + " <btaddr> <channel>"
    sys.exit(0)

btaddr = sys.argv[1]
channel = int(sys.argv[2]) or 17
running = True

sock = lightblue.socket()
sock.connect((sys.argv[1], channel))

while running:
    cmd = raw_input(">>> ")

    if cmd == "quit" or cmd == "exit":
        running = False
    else:
        sock.send(cmd)

sock.close()
