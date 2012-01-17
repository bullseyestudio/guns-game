import pygame
from modules.pgu import gui as pgui

width = 1024
height = 576
done = False

screen = None
viewport = None
background = None
font = None

tile_size = 64

zoom = 1.0
zoom_step = 0.0625

theme = None

subscreen_event_handler = None
subscreen_timer_handler = None

pguapp = pgui.App()


def draw_background():
	global screen, background, viewport

	screen.blit(background, (0,0), viewport)

def draw_background_rect(rect):
	global screen, background, viewport

	tmp = rect.copy()
	tmp.left += viewport.left
	tmp.top += viewport.top

	screen.blit(background, rect, tmp)

def scroll_background(xdist, ydist):
	global viewport

	viewport.left += xdist
	viewport.top += ydist

	viewport.left = _bounds_check(viewport.left)
	viewport.top = _bounds_check(viewport.top)

def _bounds_check(value):
	""" Helper for scroll_background, to keep it within wid/hgt + 2xtile size """
	global tile_size

	if value < 0:
		value %= tile_size
	elif value > (2 * tile_size):
		value = tile_size + (value % tile_size)

	return value


def tick_app_gfx():
	global pguapp, screen

	pguapp.update(screen)
	pygame.display.flip()

def pass_app_event(evt):
	global pguapp

	pguapp.event(evt)

def show_logo():
	logo_rect = logo.get_rect()
	logo_rect.center = screen.get_rect().center
	screen.blit(logo, logo_rect)
	pygame.display.flip()

def hide_logo():
	logo_rect = logo.get_rect()
	logo_rect.center = screen.get_rect().center
	screen.blit(background, logo_rect, logo_rect)
	pygame.display.flip()
