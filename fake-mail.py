
#!/usr/bin/python

import socket

HOST = 'localhost'
PORT = 25
MAIL_TO = "someone@on_the_inter.net"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setblocking(0)
sock.connect((HOST, PORT))

sock.send('HELO du.da')
sock.send('MAIL FROM: weihnachtsmann@nordpol.net')
print repr(sock.recv(1024))

sock.send('RCPT TO: ' + MAIL_TO)
print repr(sock.recv(1024))

sock.send('DATA')
sock.send('Subject: Dein Wunschzettel')
sock.send('Selbstverstaendlich bekommst Du Dein Pony!')
sock.send('Mfg der Weihnachtsmann')
sock.send('.')
print repr(sock.recv(1024))

sock.send('QUIT')
print repr(sock.recv(1024))

sock.close()

