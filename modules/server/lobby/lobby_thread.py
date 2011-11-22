""" Everything that gets done in the separate lobby thread.

Keep this as short as humanly possible (pick up data, queue it for handling).

"""

from modules import edicomm
from modules.server import config
from modules.server.lobby import messages, player

import threading, asyncore, asynchat, socket

class LobbyPlayerHandler(asynchat.async_chat):
	def __init__(self, sock, addr):
		asynchat.async_chat.__init__(self, sock)

		self.recv_buffer = []
		self.long_data = False

		self.addr = addr

		self.set_terminator('\n')
		return

	def set_long_data(self):
		self.long_data = True
		self.set_terminator('\n.\n')

		self.push(edicomm.encode('WAR', 1, 'Entering long data mode, end with "." by itself on a line.'))

	def collect_incoming_data(self, data):
		self.recv_buffer.append(data)

	def found_terminator(self):
		data = ''.join(self.recv_buffer)
		data = data.strip()

		if self.long_data:
			self.long_data = False
			self.set_terminator('\n')

			self.push(edicomm.encode('WAR', 2, 'Exited long data mode.'))

		messages.enqueue(self.addr, data)

		self.recv_buffer = []


class GunsLobbyDispatcher(asyncore.dispatcher):
	def __init__(self, address):
		asyncore.dispatcher.__init__(self)

		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.bind(address)
		self.address = self.socket.getsockname()
		self.listen(5)

	def handle_accept(self):
		sock, addr = self.accept()
		np = LobbyPlayerHandler(sock, addr)

		player.new(np, addr)


class GunsLobbyServer(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

		self.d = GunsLobbyDispatcher(config.listen_addr)

	def run(self):
		asyncore.loop()

server = GunsLobbyServer()
server.daemon = True
