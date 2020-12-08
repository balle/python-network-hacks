#!/usr/bin/python3

import bluetooth as bt
from signal import signal, SIGALRM, alarm
import sys

got_timeout = False
timeout = 2


def sig_alrm_handler(signum, frame):
    global got_timeout
    got_timeout = True


signal(SIGALRM, sig_alrm_handler)

if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " <addr>")
    sys.exit(0)
    
for channel in range(1, 31):
    sock = bt.BluetoothSocket(bt.RFCOMM)
    
    got_timeout = False
    channel_open = False

    try:
        alarm(timeout)
        sock.connect((sys.argv[1], channel))
        alarm(0)
        sock.close()
        channel_open = True
    except bt.btcommon.BluetoothError:
        pass

    if got_timeout:
        print("Channel " + str(channel) + " filtered")
        got_timeout = False
    elif channel_open:
        print("Channel " + str(channel) + " open")
    else:
        print("Channel " + str(channel) + " closed")
