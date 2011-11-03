""" Dispatcher class for the lobby server thread. """

import asyncore, asynchat
import socket

from player_handler import LobbyPlayerHandler
from modules import edicomm

class GunsLobbyDispatcher(asyncore.dispatcher):
	def __init__(self, address, bqueue):
		asyncore.dispatcher.__init__(self)
		self.players = []
		self.tokens = []

		self.battle_queue = bqueue

		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.bind(address)
		self.address = self.socket.getsockname()
		self.listen(5)
		self.to_battle_server( edicomm.encode('ECHO','Lobby Server Listening') )

	def handle_accept(self):
		sock, addr = self.accept()
		np = LobbyPlayerHandler(sock, addr, self)
		self.players.append(np)

	def global_chat(self, user, line):
		text = '{0}: {1}\n'.format(user, line)

		for p in self.players:
			p.push(text)

	def player_by_token(self, token):
		for p in self.players:
			if p.token == token:
				return p

	def remove_player(self, p):
		idx = self.players.index(p)
		del self.players[idx]

	def to_all(self, data):
		for p in self.players:
			p.push(data)

	def to_battle_server(self, *instr):
		for i in instr:
			self.battle_queue.put(i)

