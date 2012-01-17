""" Demo for scrolling background """

import pygame
from modules.client.gui import common
from modules.client.gui.shapes import turret
from modules.pgu import gui as pgui

hgt = common.screen.get_height()
t = pgui.Table(width=common.screen.get_width(), height=hgt)

t.tr()
t.td(pgui.Spacer(width=150, height=int(hgt) - 120), colspan=2)

t.tr()
backbtn = pgui.Button('Back to Main Menu', width=150, height=30)
t.td(backbtn)

t.tr()
t.td(pgui.Spacer(width=150, height=80), colspan=2)

initialized = False
def init():
	global initialized
	if initialized:
		return

	global backbtn
	backbtn.connect(pgui.CLICK, hide)

	initialized = True

def show():
	init()

	common.subscreen_event_handler = handle_event
	common.draw_background()
	common.pguapp.init(t, common.screen)

def hide():
	common.subscreen_event_handler = None

	import mainmenu
	mainmenu.show()

last_mpos = None
def handle_event(ev):
	if(ev.type != pygame.MOUSEMOTION):
		return

	global last_mpos
	if last_mpos:
		pos_diff = [b - a for a,b in zip(ev.pos, last_mpos)]

		common.scroll_background(*pos_diff)
		common.draw_background()
		backbtn.repaint()

	last_mpos = ev.pos
