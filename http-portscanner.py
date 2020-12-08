#!/usr/bin/python3

import sys
from socket import socket, AF_INET, SOCK_STREAM


if len(sys.argv) < 4:
    print(sys.argv[0] + ": <proxy> <port> <target>")
    sys.exit(1)

# For every interessting port
for port in (21, 22, 23, 25, 80, 443, 8080, 3128):

    # Open a TCP socket to the proxy
    sock = socket(AF_INET, SOCK_STREAM)

    try:
        sock.connect((sys.argv[1], int(sys.argv[2])))
    except ConnectionRefusedError:
        print(sys.argv[1] + ":" + sys.argv[2] + \
              " connection refused")
        break

    # Try to connect to the target and the interessting port
    print("Trying to connect to %s:%d through %s:%s" % \
          (sys.argv[3], port, sys.argv[1], sys.argv[2]))
    connect = "CONNECT " + sys.argv[3] + ":" + str(port) + \
              " HTTP/1.1\r\n\r\n"
    sock.send(connect.encode())

    resp = sock.recv(1024).decode()

    # Parse status code from http response line
    try:
        status = int(resp.split(" ")[1])
    except (IndexError, ValueError):
        status = None

    # Everything ok?
    if status == 200:
        get = "GET / HTTP/1.0\r\n\r\n"
        sock.send(get.encode())
        resp = sock.recv(1024)
        print("Port " + str(port) + " is open")
        print(resp)

    # Got error
    elif status >= 400 and status < 500:
        print("Bad proxy! Scanning denied.")
        break
    elif status >= 500:
        print("Port " + str(port) + " is closed")
    else:
        print("Unknown error! Got " + resp)

    sock.close()
