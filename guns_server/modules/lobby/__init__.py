"""Lobby state handling for Guns!, the tank game.

Runs in its own thread alongside the main thread.

"""

import Queue
import thread

class lobbyserv(object):
	def __init__(self):
		self.q = Queue.Queue()

		self.t = thread.GunsLobbyServer(self.q)
		self.t.daemon = True

	def start_listener(self):
		self.t.start()
