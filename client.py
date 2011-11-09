#!/usr/bin/env python

import sys

try:
	import pygame
	from pygame.locals import *
except ImportError:
	sys.stderr.write('This application absolutely requires pygame. Sorry.\r\n')
	sys.exit(1)

from modules import edicomm
from modules.client import config
