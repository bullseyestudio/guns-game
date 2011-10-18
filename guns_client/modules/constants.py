
try:
	import pygame.locals
except ImportError, err:
	sys.stderr.write('This application absolutely requires pygame. Sorry.\r\n')
	sys.exit(1)

players = {}
host = ''
username = ''
plr = None
screen = None
background = None
velocity = [0, 0]
font = None
joystick_count = 0
my_joystick = 0
debug_ = False
bullets = []
cplr = None
zoom = 1.0
min_zoom = 0.25
zoom_step = 0.0625


PGE_GAMETICK = pygame.locals.USEREVENT + 1

def findPlayerByName( name ):
	ret = None
	for id, p in players.iteritems():
		if not p == None:
			if p.name == name:
				ret = p
	return ret

def findPlayerById( uid ):
	ret = None
	for id, p in players.iteritems():
		if not p == None:
			if p.id == uid:
				ret = p
	return ret
