#!/usr/bin/python

import sys
import struct
import bluetooth._bluetooth as bt

if len(sys.argv) < 2:
    print sys.argv[0] + " <bdaddr>"
    sys.exit(1)

# Split bluetooth address into it's bytes
baddr = sys.argv[1].split(":")

# Open hci socket
sock = bt.hci_open_dev(0)

# CSR vendor command to change address
cmd = [ "\xc2", "\x02", "\x00", "\x0c", "\x00", "\x11",
        "\x47", "\x03", "\x70", "\x00", "\x00", "\x01",
        "\x00", "\x04", "\x00", "\x00", "\x00", "\x00",
        "\x00", "\x00", "\x00", "\x00", "\x00", "\x00",
        "\x00" ]

# Set new addr in hex
cmd[17] = baddr[3].decode("hex")
cmd[19] = baddr[5].decode("hex")
cmd[20] = baddr[4].decode("hex")
cmd[21] = baddr[2].decode("hex")
cmd[23] = baddr[1].decode("hex")
cmd[24] = baddr[0].decode("hex")

# Send HCI request
bt.hci_send_req(sock,
                bt.OGF_VENDOR_CMD,
                0,
                bt.EVT_VENDOR,
                2000,
                "".join(cmd))

sock.close()
print "Dont forget to reset your device"
