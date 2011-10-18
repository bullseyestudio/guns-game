
"""Battle state handling for Guns!, the tank game.

"""

import socket, select
import edicomm
import constants
from math import atan2, degrees

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(constants.listen_addr)

width = 2048
height = 1152

class Player:
	def __init__(self, id, token):
		self.view_offset = { 'top':10, 'left':58, 'bottom':74, 'right':10}
		self.velocity = [0,0]
		self.position = [512,384]
		self.rotation = 0
		self.zoom = 1.0
		self.view = [1024, 576]
		self.addr = None
		self.name = ''
		self.id = id
		self.token = token
		self.waypoint = None

tokens = []
players = []
to_all = []

class EDIException(Exception):
	def __init__(self, id, msg):
		Exception.__init__(self)
		self.id = id
		self.msg = msg	

class EDIData:
	def __init__(self):
		self.cmd = None
		self.pos = []
		self.id = None
		self.other = []
	def build(self, plr):
		if self.cmd != None:
			if self.cmd == 'ERR':
				return edicomm.encode(self.cmd, *self.other)
			elif self.cmd == 'USP':
				if True: #//TODO: future team check
					return edicomm.encode( self.cmd, self.id, self.pos, *self.other )
				else :
					# determine view size
					max_view_radius = [ ( int(plr.view[0]) / float(plr.zoom) ) / 2,  ( int(plr.view[1]) / float(plr.zoom) ) / 2 ]
					
					# Long-ass check for if a player is within screen view
					if self.pos[0] < ( plr.position[0] + max_view_radius[0] + plr.view_offset['right'] ) and self.pos[0] > ( plr.position[0] - max_view_radius[0] - plr.view_offset['left'] ) and self.pos[1] < ( plr.position[1] + max_view_radius[1] + plr.view_offset['top'] ) and self.pos[1] > ( plr.position[1] - max_view_radius[1] - plr.view_offset['bottom'] ):
						return edicomm.encode( self.cmd, self.id, self.pos, *self.other )
					else:
						return edicomm.encode( 'NPV', self.id )
			elif self.cmd == 'WPT':
				if self.other[0] == 'SET':
					ret = edicomm.encode(self.cmd, self.other[0], self.id, self.pos)
					return ret
				else:
					return edicomm.encode(self.cmd, self.other[0], self.id)
			else:
				return edicomm.encode(self.cmd, self.id, *self.other )
					
					

def player_by_addr(addr):
	for p in players:
		if p.addr == addr:
			return p

def player_by_token(token):
	for p in players:
		if p.token == token:
			return p

def act_on_edidata(ediparts, addr):
	global to_all
	ediparts[0] = ediparts[0].upper()

	if ediparts[0] == 'UST':
		if len(ediparts) != 2:
			raise EDIException(99, 'Wrong argument count!')

		# TODO: Validation!
		token = ediparts[1]

		print 'Got new player with token', token

		newid = 0
		if token not in tokens:
			tokens.append(token)

		newid = tokens.index(token)

		p = player_by_token(token)

		if not p:
			p = Player(newid + 1, token)
			players.append(p)

		p.addr = addr

		print 'Player (token:', token, ') got id', p.id
		sock.sendto(edicomm.encode('UID', str(p.id)), addr)
		return
	elif ediparts[0] == 'USN':
		if len(ediparts) != 2:
			raise EDIException(99, 'Wrong argument count!')

		p = player_by_addr(addr)

		if p == None:
			raise EDIException(100, 'Please re-authenticate')

		# TODO: Validation!
		newname = ediparts[1]

		print 'Player', p.id, 'sets name to', newname, 'from', p.name

		p.name = newname

		to_all.append(edicomm.encode('USN', str(p.id), p.name))

		lines = [edicomm.encode('USN', pl.id, pl.name) for pl in players if pl.id != p.id and pl.name != '']
		sock.sendto('\n'.join(lines), addr)

	elif ediparts[0] == 'USD':
		p = player_by_addr(addr)

		if p == None:
			raise EDIException(100, 'Please re-authenticate')

		print 'Player', p.name, 'disconnects'

		players.remove(p)
		to_all.append(edicomm.encode('USD', str(p.id)))

	elif ediparts[0] == 'USV':
		p = player_by_addr(addr)

		if p == None:
			raise EDIException(100, 'Please re-authenticate')

		if len(ediparts) != 2:
			raise EDIException(99, 'Wrong argument count!')

		p.velocity = [int(x) for x in ediparts[1]]

		print 'Player', p.name, 'velocity change:', p.velocity
	elif ediparts[0] == 'USF':
		p = player_by_addr(addr)

		if p == None:
			raise EDIException(100, 'Please re-authenticate')

		if len(ediparts) != 2:
			raise EDIException(99, 'Wrong argument count!')

		desired_shot = [int(x) for x in ediparts[1]]
		#to_all.append(edicomm.encode('USF', str(p.id), desired_shot))
		dat = EDIData()
		dat.cmd = 'USF'
		dat.id = str(p.id)
		dat.other.append( desired_shot )
		
		to_all.append( dat )
	elif ediparts[0] == 'USR':
		p = player_by_addr(addr)
		
		if p == None:
			raise EDIException(100, 'Please re-authenticate')
		
		p.view = ediparts[1]
	elif ediparts[0] == 'USZ':
		p = player_by_addr(addr)
		
		if p == None:
			raise EDIException(100, 'Please re-authenticate')
		
		p.zoom = ediparts[1]
	elif ediparts[0] == 'WPT':
		p = player_by_addr(addr)
		
		if ediparts[1] == 'SET':
			p.waypoint = ediparts[2]
			dat = EDIData()
			dat.cmd = 'WPT'
			dat.pos = ediparts[2]
			dat.other.append( 'SET' )
			dat.id = p.id
			
			to_all.append( dat )
		elif ediparts[1] == 'UNSET':
			p.waypoint = None
			dat = EDIData()
			dat.cmd = 'WPT'
			dat.other.append( 'UNSET' )
			dat.id = p.id
			
			to_all.append( dat )
		else:
			print 'Unhandled WPT: {0}'.format( ediparts[1] )
			

def check_for_playerinput():
	while True:
		socks = select.select([sock], [], [], 0)

		if len(socks[0]) == 0:
			return

		data, addr = sock.recvfrom(1500)
		data = data.strip()
		print 'got data: ', data, 'from', addr

		try:
			act_on_edidata(edicomm.decode(data), addr)
		except EDIException as e:
			sock.sendto(edicomm.encode('ERR', str(e.id), e.msg), addr)

def move_players():
	global to_all

	for p in players:
		newpos = [(vel / 10) + pos for(vel, pos) in zip(p.velocity, p.position)]

		if newpos[0] < 0 or newpos[0] > width:
			p.velocity[0] = 0
			newpos[0] = p.position[0]
		if newpos[1] < 0 or newpos[1] > height:
			p.velocity[1] = 0
			newpos[1] = p.position[1]

		newrot = p.rotation

		if p.velocity != [0,0]:
			newrot = degrees(atan2(p.velocity[0], p.velocity[1]))

		p.position = newpos
		p.rotation = newrot

		to_all.append(edicomm.encode('USP', p.id, p.position, p.rotation))

def tell_players():
	global to_all
	if len(to_all) < 1:
		return

	#data = '\n'.join(to_all)
	#to_all = []

	for p in players:
		if p.name != '':
			data = []
			for dat in to_all:
				d = dat.build(p)
				if d != None:
					data.append( d )
			data = '\n'.join(data)
			sock.sendto(data, p.addr)

	to_all = []

def timer_tick():
	check_for_playerinput()
	move_players()
	tell_players()
