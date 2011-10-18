
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
spawn = [ width/2, height/2 ]

class Player:
	def __init__(self, id, token):
		self.view_offset = { 'top':10, 'left':58, 'bottom':74, 'right':10}
		self.velocity = [0,0]
		self.position = [512,384]
		self.rotation = 0
		self.tankshape = [0,0,48,64]
		self.zoom = 1.0
		self.view = [1024, 576]
		self.addr = None
		self.name = ''
		self.id = id
		self.token = token
		self.waypoint = None
	def contains(self, pos):
		deltax = pos[0] - self.position[0]
		deltay = pos[1] - self.position[1]

		if( deltax > 0 and deltax < self.tankshape[2]
		and deltay > 0 and deltay < self.tankshape[3]):
			return True
		else:
			return False

class Waypoint:
	def __init__(self, id, pos, name):
		self.title = name
		self.position = pos
		self.id = id

tokens = []
players = []
waypoints = []
to_all = []

class EDIException(Exception):
	def __init__(self, id, msg):
		Exception.__init__(self)
		self.id = id
		self.msg = msg

def player_by_addr(addr):
	for p in players:
		if p.addr == addr:
			return p

def player_by_token(token):
	for p in players:
		if p.token == token:
			return p

def wp_by_id( id ):
	for w in waypoints:
		if w.id == id:
			return w

def wp_idx_by_id( id ):
	for w in waypoints:
		if w.id == id:
			return waypoints.index( w )

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
		wplines = [edicomm.encode('WPT', wp.id, wp.position, wp.title) for wp in waypoints]
		lines.extend(wplines)
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
		for pl in players:
			if not pl.id == p.id and pl.contains( desired_shot ):
				pl.position = spawn
		to_all.append(edicomm.encode('USF', str(p.id), desired_shot))

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

		if p == None:
			raise EDIException(100, 'Please re-authenticate')

		if len(ediparts) == 2: # Player wants waypoint set: WPT x,y
			wpid = constants.min_player_wpid + p.id
			wppos = [int(x) for x in ediparts[1]]
			wptitle = constants.player_wp_fmtstring.format(p=p)
			
			wpidx = wp_idx_by_id( wpid )
			if not wpidx == None:
				del waypoints[ wpidx ]
			waypoints.append( Waypoint( wpid, wppos, wptitle ) )
			
			to_all.append(edicomm.encode('WPT', wpid, wppos, wptitle))
		elif len(ediparts) == 1: # Player wants waypoint deleted
			wpid = constants.min_player_wpid + p.id
			
			wpidx = wp_idx_by_id( wpid )
			
			del waypoints[ wpidx ]

			to_all.append(edicomm.encode('WPT', wpid))
		else:
			print 'Malformed WPT: {0}'.format( edicomm.encode(ediparts) )
			raise EDIException(99, 'Wrong argument count!')


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

	data = '\n'.join(to_all)

	for p in players:
		if p.name != '':
			sock.sendto(data, p.addr)

	to_all = []

def timer_tick():
	check_for_playerinput()
	move_players()
	tell_players()
