""" Dispatcher class for the lobby server thread. """

import asyncore, asynchat
import socket

import player_handler

class GunsLobbyDispatcher(asyncore.dispatcher):
	def __init__(self, address, queue):
		asyncore.dispatcher.__init__(self)
		self.queue = queue
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.bind(address)
		self.address = self.socket.getsockname()
		self.listen(5)
		return

	def handle_accept(self):
		sock, addr = self.accept()
		np = LobbyPlayerHandler(sock, addr, self.queue)
		all_players.append(np)
