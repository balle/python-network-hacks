#!/usr/bin/python

import socket

HOST = 'localhost'
PORT = 1337

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

conn, addr = s.accept()

print 'Connected by', addr

while 1:
    data = conn.recv(1024)
    if not data: break
    conn.send(data)

conn.close()

