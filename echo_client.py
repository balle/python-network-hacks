#!/usr/bin/python

import socket

HOST = 'localhost'
PORT = 1337

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

s.send('Hello, world')
data = s.recv(1024)

s.close()
print 'Received', repr(data)

