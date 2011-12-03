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

def show_optsmenu():
	""" Show the options screen """
	from modules.client.gui import optsmenu
	global pguapp, screen

	draw_background()
	pguapp.init(optsmenu.t, screen)

def show_mpmenu():
	""" Show the multiplayer screen """
	from modules.client.gui import mpmenu
	from modules.client import gui
	global pguapp, screen

	gui.subscreen_update = None
	draw_background()
	pguapp.init(mpmenu.t, screen)

def show_status():
	""" Show the multiplayer screen """
	from modules.client.gui import status
	global pguapp, screen

	draw_background()
	pguapp.init(status.t, screen)

	from modules.client import lobby
	lobby.start()

def show_mainmenu():
	""" Main screen turn on """
	from modules.client.gui import mainmenu
	from modules.client import gui
	global pguapp, screen

	gui.subscreen_update = None
	draw_background()
	pguapp.init(mainmenu.t, screen)

def show_turrets():
	""" Show the turrets demo """
	from modules.client.gui import turrets
	from modules.client import gui
	global pguapp, screen

	gui.subscreen_update = turrets.draw_turrets
	draw_background()
	pguapp.init(turrets.t, screen)

def show_bgdemo():
	""" Show the background demo """
	from modules.client.gui import bgdemo
	from modules.client import gui
	global pguapp, screen

	gui.subscreen_update = bgdemo.draw_bg
	draw_background()
	pguapp.init(bgdemo.t, screen)

def show_lobby():
	""" Show the lobby screen """
	from modules.client.gui import lobby
	from modules.client import lobby as lobbyserv
	from modules.client import gui
	global pguapp, screen

	gui.subscreen_update = lobbyserv.tick
	draw_background()
	pguapp.init(lobby.t, screen)


def tick_app_gfx():
	global pguapp, screen

	rects = pguapp.update(screen)
	pygame.display.flip()

def pass_app_event(evt):
	global pguapp

	pguapp.event(evt)
