#!/usr/bin/env python

import sys, time

try:
	import pygame
	import pygame._view # Py2exe needs this, else it won't include _view
	from pygame.locals import *
except ImportError:
	sys.stderr.write('This application absolutely requires pygame. Sorry.\r\n')
	sys.exit(1)

pygame.init()

from modules import edicomm
from modules.client import config, gui

config.read_config()
gui.init_display()
gui.show_logo()
ms_atlogo = pygame.time.get_ticks()

# Q'n'D demo code (delete me soonest)
from modules.client.gui import mainmenu
from modules.pgu import gui as pgui

a = pgui.App()

a.init(mainmenu.t, gui.common.screen)

ms_afterinit = pygame.time.get_ticks()
ms_to_wait = 2000 - (ms_afterinit - ms_atlogo)
pygame.time.wait(ms_to_wait)

gui.hide_logo()
a.loop()

c = pygame.time.Clock()

quitting = False
while not quitting:
	elapsed = c.tick(60)

	for ev in pygame.event.get():
		if ev.type == pygame.QUIT:
			quitting = True

		a.event(ev)

	rects = a.update(gui.common.screen)
	pygame.display.update(rects)
# End Q'n'D demo code
