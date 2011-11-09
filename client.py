#!/usr/bin/env python

import sys, time

try:
	import pygame
	from pygame.locals import *
except ImportError:
	sys.stderr.write('This application absolutely requires pygame. Sorry.\r\n')
	sys.exit(1)

pygame.init()

from modules import edicomm
from modules.client import config, gui

config.read_config()
gui.init_display()

# Q'n'D demo code (delete me soonest)
from modules.client.gui import common
for i in range(0, 64):
	gui.common.viewport.top = i
	gui.common.viewport.left = i

	common.screen.blit(common.background, (0,0), common.viewport)
	pygame.display.flip()

	time.sleep(0.01)
# End Q'n'D demo code

time.sleep(2)
