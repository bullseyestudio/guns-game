#!/usr/bin/env python

import socket
import select

LISTEN_HOST = '0.0.0.0'
LISTEN_PORT = 45005

BUFFER_SIZE = 1024

socks = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((LISTEN_HOST, LISTEN_PORT))
s.listen(5)

socks.append(s)

while True:
	to_send = ""

	socks_to_read, socks_to_write, socks_to_err = select.select(socks, [], socks, 0.1)

	socks_to_write = socks

	if len(socks_to_read) < 1:
		continue

	if s in socks_to_read:
		conn, addr = s.accept()
		print 'Accepted connection from:', addr
		socks.append(conn)
		socks_to_read.remove(s)

	for sock in socks_to_read:
		data = sock.recv(BUFFER_SIZE)
		if not data:
			print 'Connection closed. I dunno which.'
			socks_to_write.remove(sock)
			socks.remove(sock)
			sock.close()
			continue

		print 'Received:', data

		to_send += data

	for sock in socks_to_write:
		if sock == s:
			continue
		sock.send(to_send)

# cleanup
for sock in socks:
	sock.close()
