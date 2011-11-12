import pygame

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

from modules.pgu import gui as pgui
pguapp = pgui.App()

def draw_background():
	global screen, background, viewport

	screen.blit(background, (0,0), viewport)
	pygame.display.flip()

def show_optsmenu():
	""" Show the options screen """
	from modules.client.gui import optsmenu
	global pguapp, screen

	draw_background()
	pguapp.init(optsmenu.t, screen)

def show_mainmenu():
	""" Main screen turn on """
	from modules.client.gui import mainmenu
	global pguapp, screen

	draw_background()
	pguapp.init(mainmenu.t, screen)

def tick_app_gfx():
	global pguapp, screen

	rects = pguapp.update(screen)
	pygame.display.update(rects)

def pass_app_event(evt):
	global pguapp

	pguapp.event(evt)
