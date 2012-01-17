import pygame

from modules import edicomm
from modules.client import config, gui

def init():
	config.read_config()
	gui.init_display()
	gui.show_logo()
	ms_atlogo = pygame.time.get_ticks()

	gui.init_app()

	# Any other init stuff that can go in here should do so.

	from modules.client.gui import mainmenu
	mainmenu.init()

	ms_afterinit = pygame.time.get_ticks()
	ms_to_wait = 2000 - (ms_afterinit - ms_atlogo)
	pygame.time.wait(ms_to_wait) # We do want people to see our nice logo :)

	gui.hide_logo()

	mainmenu.show()
	#gui.tick_app_gfx()

quitting = False

def tick(elapsed):
	global quitting

	for ev in pygame.event.get():
		if ev.type == pygame.QUIT:
			quitting = True

		if gui.common.subscreen_event_handler:
			gui.common.subscreen_event_handler(ev)

		gui.pass_app_event(ev)

	if gui.common.subscreen_timer_handler:
		gui.common.subscreen_timer_handler(elapsed)

	gui.tick_app_gfx()

def exit():
	# Any other exit stuff that can go in here should do so.
	config.write_config()
