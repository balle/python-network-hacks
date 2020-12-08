
#!/usr/bin/python3

import socket

HOST = 'mx1.codekid.net'
PORT = 25
MAIL_TO = "<someone@on_the_inter.net>"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

sock.send('HELO du.da'.encode())
sock.send('MAIL FROM: <santaclaus@northpole.net>'.encode())
print(sock.recv(1024).decode())

sock.send('RCPT TO: '.encode() + MAIL_TO.encode())
print(sock.recv(1024).decode())

sock.send('DATA'.encode())
sock.send('Subject: Your wishlist'.encode())
sock.send('Of course you get your pony!'.encode())
sock.send('Best regards Santa'.encode())
sock.send('.'.encode())
print(sock.recv(1024).decode())

sock.send('QUIT'.encode())
print(sock.recv(1024).decode())

sock.close()
