import pygame.locals

host = ''
username = ''

screen = None
background = None
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
