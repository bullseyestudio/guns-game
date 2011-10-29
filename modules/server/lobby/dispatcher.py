""" Dispatcher class for the lobby server thread. """

import asyncore, asynchat
import socket

from player_handler import LobbyPlayerHandler

class GunsLobbyDispatcher(asyncore.dispatcher):
	def __init__(self, address):
		asyncore.dispatcher.__init__(self)
		self.players = []

		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.bind(address)
		self.address = self.socket.getsockname()
		self.listen(5)

	def handle_accept(self):
		sock, addr = self.accept()
		np = LobbyPlayerHandler(sock, addr, self)
		self.players.append(np)

	def global_chat(self, user, line):
		text = '{0}: {1}\n'.format(user, line)

		for p in self.players:
			p.push(text)
