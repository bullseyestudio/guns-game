#!/usr/bin/env python

import sys, os

sys.path.append('./modules')
sys.path.append('../common/modules')

try:
	import pygame
	from pygame.locals import *
except ImportError, err:
	sys.stderr.write('This application absolutely requires pygame. Sorry.\r\n')
	sys.exit(1)

import pgu.gui as gui

size = (1024, 576)

# Initialise screen
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Guns! Build-a-Tank preview')

app = gui.App()

# Two surfaces: viewing area and parts bin; 80-20 split?
#Maybe need a third surface for the status mini-view? To get people used to it, I mean.
va_size = (int(size[0] * 0.8), size[1])
pb_size = (size[0] - va_size[0], size[1])

viewarea = pygame.Surface(va_size)
viewarea.convert()
viewarea.fill((0, 0, 0))

partsbin = pygame.Surface(pb_size)
partsbin.convert()
partsbin.fill((0, 0, 250))

font = pygame.font.Font(None, 36)
textcolor = ( 255, 255, 255 )

text = font.render( "View Area", 1, textcolor )
viewarea.blit(text, (10,10), text.get_rect())

text = font.render( "Parts Bin", 1, textcolor )
partsbin.blit(text, (10,10), text.get_rect())

butt = gui.Button("Hello, world", x=10, y=48, width=128, height=16)
c = gui.Container(align=-1,valign=-1)
c.add(butt, 10,48)
app.init(c)

print viewarea.get_rect(), partsbin.get_rect()

# Blit everything to the screen
screen.blit(viewarea, (pb_size[0], 0), viewarea.get_rect())
screen.blit(partsbin, (0, 0), partsbin.get_rect())
pygame.display.flip()

done = False
while not done:
	for event in pygame.event.get():
		if (event.type == QUIT):
			done = True
		elif event.type is KEYDOWN and event.key == K_ESCAPE:
			done = True
		else:
			app.event(event)

	app.paint()
	pygame.display.flip()
