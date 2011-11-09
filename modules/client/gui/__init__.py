import pygame
import math

from modules.client import config
from modules.client.gui import common

__all__ = ['common']

def init_display():
	width = config.cp.getint('window', 'width')
	height = config.cp.getint('window', 'height')

	common.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
	common.viewport = common.screen.get_rect()
	pygame.display.set_caption("Guns! the tank game v0.1 ALPHA")

	common.font = pygame.font.Font(None, 18)

	redraw_background()

	common.screen.blit(common.background, (0,0), common.viewport)
	pygame.display.flip()

def resize_display(newsize):
	common.screen = pygame.display.set_mode(newsize, pygame.RESIZABLE)
	common.viewport.width = screen.get_width()
	common.viewport.height = screen.get_height()

	redraw_background()

def redraw_background():
	common.tile_size = int(64 * common.zoom)

	tile_size = common.tile_size
	tile = pygame.Surface((tile_size, tile_size)).convert()
	tile.fill((250,250,250))

	pointlist = ((0,tile_size - 1), (tile_size - 1,tile_size - 1), (tile_size - 1,0))
	pygame.draw.lines(tile, (0,0,0), False, pointlist)

	# Background is bigger than it needs to be to allow for scrolling it without
	#rebuilding it every damn time -- just move the viewport and re-blit
	bgsize = [x + (tile_size * 2) for x in common.screen.get_size()]

	common.background = pygame.Surface(bgsize).convert()

	common.viewport.top = common.tile_size
	common.viewport.left = common.tile_size

	rowcount = int(math.ceil(common.background.get_height() / tile_size))
	colcount = int(math.ceil(common.background.get_width() / tile_size))

	for row in range(0, rowcount):
		for col in range(0, colcount):
			common.background.blit(tile, (col * tile_size, row * tile_size))
