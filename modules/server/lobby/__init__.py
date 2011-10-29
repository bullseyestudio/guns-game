""" Lobby state handling for Guns!, the tank game.

Runs in its own thread alongside the main thread.

"""

import threading, asyncore

from modules.server import constants
import dispatcher

class GunsLobbyServer(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

		self.d = dispatcher.GunsLobbyDispatcher(constants.listen_addr)

	def run(self):
		asyncore.loop()

server = GunsLobbyServer()
server.daemon = True

def start_server():
	global server
	server.start()

	print 'Lobby server thread started.'
