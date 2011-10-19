import locals, waypoint, network
import edicomm
import pygame

from math import degrees, atan2

from locals import PlayerAmbiguityError # raised by by_partial_name

class Player:
	def __init__(self, id, token):
		self.velocity = [0,0]
		self.position = list(locals.spawn)
		self.rotation = 0

		# Q'n'D collision detection
		self.tank_rect = pygame.Rect(locals.spawn,(48,48))

		self.zoom = 1.0
		self.viewport = [1024, 576]

		self.addr = None

		self.name = ''
		self.id = id
		self.token = token

		self.waypoint = None

		self.lines = []
		self.ready = False

	def can_see(self, p):
		if not self.ready: # Players who aren't ready can't see anyone
			return False

		if not p.ready: # Nobody can see players who aren't ready
			return False

		# TODO: Determine if player is visible!
		return True

	def can_see_at(self, coords):
		if not self.ready: # Players who aren't ready can't see anything
			return False

		# TODO: Determine if coordinates are visible!
		return True

	def contains(self, pos):
		return self.tank_rect.collidepoint(pos)

	def enqueue(self, str):
		self.lines.append(str)

	def move(self):
		if not self.ready:
			return

		newpos = [int(vel / 10) + pos for(vel, pos) in zip(self.velocity, self.position)]

		if newpos[0] < 0 or newpos[0] > locals.width:
			self.velocity[0] = 0
			newpos[0] = self.position[0]
		if newpos[1] < 0 or newpos[1] > locals.height:
			self.velocity[1] = 0
			newpos[1] = self.position[1]

		newrot = self.rotation

		if self.velocity != [0,0]:
			newrot = degrees(atan2(self.velocity[0], self.velocity[1]))

		self.position = newpos
		self.rotation = newrot

		self.tank_rect.topleft = newpos

		network.to_observing(self, edicomm.encode('USP', self.id, self.position, self.rotation))

	def transmit(self):
		if (len(self.lines) == 0) or (self.addr == None):
			return

		data = '\n'.join(self.lines)

		network.sock.sendto(data, self.addr)

		self.lines = []

all = []
tokens = []

def new_player(id, token):
	p = Player(id, token)
	all.append(p)

	return p

def by_addr(addr):
	global all

	for p in all:
		if p.addr == addr:
			return p

def by_token(token):
	global all

	for p in all:
		if p.token == token:
			return p

def by_partial_name(str):
	"""
		Self-explanatory, but note: will raise locals.PlayerAmbiguityError if
		partial name matches multiple choices
	"""
	global all

	found_p = None

	for p in all:
		if p.name.lower() == parts[1].lower(): #exact match!
			return p
		elif p.name.lower().startswith(parts[1].lower()): # name starts with str
			if found_p != None:
				raise PlayerAmbiguityError(found_p, p)
			else:
				found_p = p

	return p


def move_all():
	global all

	for p in all:
		p.move()

def xmit_all():
	global all

	for p in all:
		p.transmit()
