""" Player handler class -- a new one of these is spawned for every
connection to the dispatcher.

"""

import edicomm

import asynchat

class LobbyPlayerHandler(asynchat.async_chat):
	def __init__(self, sock, addr, queue):
		self.recv_buffer = []
		self.queue = queue
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
		ediparts = edicomm.decode(line)

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
