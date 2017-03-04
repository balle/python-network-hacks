#!/usr/bin/python

import lightblue

for device in lightblue.finddevices():
    print device[0] + " " + device[1]
