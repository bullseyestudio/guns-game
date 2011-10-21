""" Player handler class -- a new one of these is spawned for every
connection to the dispatcher.

"""

from modules import edicomm

import asynchat, pygame

class LobbyPlayerHandler(asynchat.async_chat):
	def __init__(self, sock, addr, dispatcher):
		self.recv_buffer = []
		self.dispatcher = dispatcher
		self.username = ''

		asynchat.async_chat.__init__(self, sock)
		self.set_terminator('\n')
		return

	def collect_incoming_data(self, data):
		self.recv_buffer.append(data)

	def found_terminator(self):
		self.process_command()

	def process_command(self):
		line = ''.join(self.recv_buffer)
		line = line.strip()

		ediparts = edicomm.decode(line)

		if isinstance(ediparts[0], basestring):
			ediparts[0] = ediparts[0].upper()

		if ediparts[0] == 'USR':
			self.username = ediparts[1]
			self.push('+OK Your username set to: ' + self.username + '\n')
		elif ediparts[0] == 'WHO':
			self.push('+OK You are: ' + self.username + '\n')
		elif ediparts[0] == 'BYE':
			self.push('+OK Goodbye now.\n')
			self.close_when_done()
		elif ediparts[0] == 'DIE':
			if self.username == 'narc':
				pygame.event.post(pygame.event.Event(pygame.locals.QUIT))
				self.push('+OK Going to die now.\n')
			else:
				self.push('-ERR You are not narc!\n')
		else:
			self.dispatcher.global_chat(self.username, line)

		self.recv_buffer = []
