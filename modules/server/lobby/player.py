from modules import edicomm
from modules.server import auth
from modules.server.battle.player import tokens

class Player:
	def __init__(self, handler, addr):
		self.handler = handler
		self.addr = addr

		self.nick = None
		self.metanick = None

	def process_message(self, msg):
		# TODO: Handle long data (currently unused, but support is built-in)
		ediparts = edicomm.decode(msg.data)

		ediparts[0] = ediparts[0].upper()

		if ediparts[0] == 'USN':
			self.new_nick(ediparts[1])

	def enqueue(self, msg):
		self.handler.push(msg + '\n')

	def new_nick(self, nick):
		if not self.nick: # First-time setting?
			self.metanick = nick
			tok = auth.player_token(nick)
			tokens.append(tok)
			self.enqueue(edicomm.encode('TOK', tok))

		self.nick = nick
		self.enqueue(edicomm.encode('USN', nick))

	def get_lost(self):
		global all

		self.handler.push('+OK Goodbye now.\n')
		self.handler.close_when_done()
		all.remove(self)


all = []

def new(handler, addr):
	p = Player(handler, addr)
	all.append(p)

	return p

def by_addr(addr):
	global all

	for p in all:
		if p.addr == addr:
			return p

	return None
