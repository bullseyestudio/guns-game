import pygame
from pygame.locals import *

import battle
import network_comms
import constants
import input_handler

rang = 0

def draw_rot():
	global rang
	srf = pygame.Surface( ( 288, 288 ) )
	srf.fill( (255, 0, 255 ) )
	srf.set_colorkey( (255, 0, 255 ) )
	pygame.draw.rect( srf, (255, 0, 0), (144-32, 144-32, 64, 64), 3 )
	srf2 = pygame.transform.rotate( srf, rang )
	rang = rang + 0.1
	constants.screen.blit( srf,  (100, 100) )
	xp = 400 - ( srf2.get_width() / 2 )
	yp = 100 - ( srf2.get_height() / 2 )
#	constants.screen.blit( constants.background, (xp, yp), (xp, yp, srf2.get_width(), srf2.get_height()))
	constants.screen.blit( srf2, (xp, yp) )
