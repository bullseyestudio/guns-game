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
gui.show_logo()

# Q'n'D demo code (delete me soonest)
from modules.client.gui import mainmenu
from modules.pgu import gui as pgui

a = pgui.App()
a.connect(pgui.QUIT, a.quit, None)
mainmenu.b.connect(pgui.CLICK,a.quit,None)

gui.hide_logo()

a.run(mainmenu.t)
# End Q'n'D demo code
