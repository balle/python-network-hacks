#!/usr/bin/python3

from wifi import Cell

iface = "wlp2s0"

for cell in Cell.all(iface):
    output = "%s\t(%s)\tchannel %d\tsignal %d\tmode %s " % \
        (cell.ssid, cell.address, cell.channel, cell.signal, cell.mode)

    if cell.encrypted:
        output += "(%s)" % (cell.encryption_type.upper(),)
    else:
        output += "(Open)"

    print(output)
    
