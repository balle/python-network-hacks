#!/usr/bin/python

import sys
from scapy.layers.l2 import Dot3 , LLC, SNAP
from scapy.contrib.dtp import *

if len(sys.argv) < 2:
    print sys.argv[0] + " <dev>"
    sys.exit()

negotiate_trunk(iface=sys.argv[1])
