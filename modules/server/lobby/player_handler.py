""" Player handler class -- a new one of these is spawned for every
connection to the dispatcher.

"""

from modules import edicomm

import asynchat, pygame, md5

class LobbyPlayerHandler(asynchat.async_chat):
	def __init__(self, sock, addr, dispatcher):
		self.recv_buffer = []
		self.dispatcher = dispatcher
		self.username = ''
		self.token = ''
		self.id = None

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

		if ediparts[0] == 'USN':
			self.username = ediparts[1]
			self.generate_token()

			nid = None
			for t in self.dispatcher.tokens:
				if t == self.token:
					nid = self.dispatcher.tokens.index(t)
					self.dispatcher.remove_player(self.dispatcher.player_by_token(t))

			if nid == None:
				nid = len(self.dispatcher.tokens)
				self.dispatcher.tokens.append(self.token)
			self.id = nid+1

			self.dispatcher.to_battle_server( edicomm.encode('USR',self.id,self.username,self.token) )

			nickmap = [edicomm.encode('USN', pl.id, pl.username) for pl in self.dispatcher.players]

			self.push( edicomm.encode('UID',self.id) + '\n' )
			self.push( edicomm.encode('UST',self.token) + '\n' )
			self.push( '\n'.join(nickmap) + '\n' )

			self.dispatcher.to_all( edicomm.encode('USN', self.id, self.username) )
		elif ediparts[0] == 'USD':
			self.dispatcher.to_battle_server( edicomm.encode('ECHO', '{0} disconnected!'.format(self.username)) )
			self.dispatcher.to_battle_server( edicomm.encode('USD',self.id, ediparts[1]) )
			self.dispatcher.to_all( edicomm.encode('USD',self.id, ediparts[1]) )
			del self.dispatcher.tokens[ self.dispatcker.tokens.index(self.token) ]
			self.dispatcher.remove_player(self.dispatcher.player_by_token(t))
		elif ediparts[0] == 'USR':
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

	def generate_token(self):
		token = md5.new('token_{0}'.format(self.username)).digest();
		self.token = token
