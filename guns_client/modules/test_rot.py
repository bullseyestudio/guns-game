
import sys

sys.path.append('./modules')
sys.path.append('../common/modules')

import battle
import network_comms
import global_
from global_ import *
import input_handler

try:
	import pygame
	from pygame.locals import *
except ImportError, err:
	sys.stderr.write('This application absolutely requires pygame. Sorry.\r\n')
	sys.exit(1)

rang = 0

def draw_rot():
	global rang
	srf = pygame.Surface( ( 288, 288 ) )
	srf.fill( (255, 0, 255 ) )
	srf.set_colorkey( (255, 0, 255 ) )
	pygame.draw.rect( srf, (255, 0, 0), (144-32, 144-32, 64, 64), 1 )
	srf2 = pygame.transform.rotate( srf, rang )
	rang = rang + 0.1
	global_.screen.blit( srf,  (100, 100) )
	xp = 400 - ( srf2.get_width() / 2 )
	yp = 100 - ( srf2.get_height() / 2 )
#	global_.screen.blit( global_.background, (xp, yp), (xp, yp, srf2.get_width(), srf2.get_height()))
	global_.screen.blit( srf2, (xp, yp) )
