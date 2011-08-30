#!/usr/bin/env python

import asyncore, asynchat
import socket # for socket.AF_*, socket.SOCK_*

all_players = []

def global_chat(message):
	for p in all_players:
		p.push(message)

def global_shutdown():
	for p in all_players:
		p.push('Server is shutting down now!\r\n')
		p.close_when_done()

	server.close()

class LobbyPlayerHandler(asynchat.async_chat):
	def __init__(self, sock, addr):
		self.recv_buffer = []
		asynchat.async_chat.__init__(self, sock)
		self.set_terminator('\n')
		self.username = ''
		return

	def collect_incoming_data(self, data):
		self.recv_buffer.append(data)

	def found_terminator(self):
		self.process_command()

	def process_command(self):
		line = ''.join(self.recv_buffer)
		line_parts = line.strip().split(None, 1)

		if len(line_parts) == 1:
			verb = line_parts[0].upper()
			arg = ''
		else:
			verb = line_parts[0].upper()
			arg = line_parts[1]

		if 'USER'.startswith(verb):
			self.username = arg
			self.push('+OK Your username set to: ' + self.username + '\r\n')
		elif 'WHOAMI'.startswith(verb):
			self.push('+OK You are: ' + self.username + '\r\n')
		elif 'QUIT'.startswith(verb):
			self.push('+OK Goodbye now.\r\n')
			self.close_when_done()
		elif 'SHUTDOWN'.startswith(verb):
			if self.username == 'narc':
				global_shutdown()
			else:
				self.push('-ERR You are not narc!\r\n')
		else:
			global_chat(self.username + ': ' + line.strip() + '\r\n')

		self.recv_buffer = []


class GunsServer(asyncore.dispatcher):
	def __init__(self, address):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.bind(address)
		self.address = self.socket.getsockname()
		self.listen(5)
		return

	def handle_accept(self):
		sock, addr = self.accept()
		np = LobbyPlayerHandler(sock, addr)
		all_players.append(np)

address = ('0.0.0.0', 45005)
server = GunsServer(address)

asyncore.loop()
