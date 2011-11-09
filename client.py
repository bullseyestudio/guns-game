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
time.sleep(1)

for i in range(0, 256):
	gui.scroll_background(1, 2)
	gui.draw_background()

	time.sleep(0.01)
# End Q'n'D demo code

time.sleep(2)
