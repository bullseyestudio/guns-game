""" Thread class to be spawned by the lobby server. """

import threading

from .. import constants
import dispatcher

class GunsLobbyServer(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue
		self.finished = False

		self.d = dispatcher.GunsLobbyDispatcher(constants.listen_addr, self.queue)
