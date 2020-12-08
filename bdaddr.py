#!/usr/bin/python3

import sys
import struct
import bluetooth._bluetooth as bt
import codecs

if len(sys.argv) < 2:
    print(sys.argv[0] + " <bdaddr>")
    sys.exit(1)

# Split bluetooth address into it's bytes
baddr = sys.argv[1].split(":")

# Open hci socket
sock = bt.hci_open_dev(1)

# CSR vendor command to change address
cmd = [ b"\xc2", b"\x02", b"\x00", b"\x0c", b"\x00", b"\x11",
        b"\x47", b"\x03", b"\x70", b"\x00", b"\x00", b"\x01",
        b"\x00", b"\x04", b"\x00", b"\x00", b"\x00", b"\x00",
        b"\x00", b"\x00", b"\x00", b"\x00", b"\x00", b"\x00",
        b"\x00" ]

# Set new addr in hex
decode_hex = codecs.getdecoder("hex_codec")

cmd[17] = decode_hex(baddr[3])[0]
cmd[19] = decode_hex(baddr[5])[0]
cmd[20] = decode_hex(baddr[4])[0]
cmd[21] = decode_hex(baddr[2])[0]
cmd[23] = decode_hex(baddr[1])[0]
cmd[24] = decode_hex(baddr[0])[0]

# Send HCI request
bt.hci_send_req(sock,
                bt.OGF_VENDOR_CMD,
                0,
                bt.EVT_VENDOR,
                2000,
                b"".join(cmd))

sock.close()
print("Dont forget to reset your device")
