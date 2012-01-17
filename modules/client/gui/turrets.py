""" Demo for tracking turrets """

import pygame
from modules.client.gui import common
from modules.client.gui.shapes import turret, bullet
from modules.pgu import gui as pgui
from modules.client import config

hgt = common.screen.get_height()
t = pgui.Table(width=common.screen.get_width(), height=hgt)

t.tr()
t.td(pgui.Spacer(width=150, height=int(hgt) - 120), colspan=2)

t.tr()
backbtn = pgui.Button('Back to Main Menu', width=150, height=30)
t.td(backbtn)

t.tr()
t.td(pgui.Spacer(width=150, height=80), colspan=2)

turr = turret.Turret(common.screen, (128,128))
turr2 = turret.Turret(common.screen, (530,255))
shooting = False

initialized = False
def init():
	global initialized
	if initialized:
		return

	global backbtn
	backbtn.connect(pgui.CLICK, hide)

	initialized = True

def event_handler(ev):
	global shooting, turr, turr2

	if(ev.type == pygame.MOUSEMOTION):
		turr.point_at(ev.pos)
		turr2.point_at(ev.pos)
	elif(ev.type == pygame.MOUSEBUTTONDOWN):
		if(backbtn.is_hovering()):
			return

		shooting = True
	elif(ev.type == pygame.MOUSEBUTTONUP) and shooting:
		shooting = False

def timer_tick(elapsed):
	global shooting, turr, turr2

	if shooting:
		turr.fire()
		turr2.fire()
	for b in bullet.all:
		b.unrender()
	turr.paint()
	turr2.paint()
	for b in bullet.all:
		b.think()
		b.render()

def show():
	init()

	common.subscreen_event_handler = event_handler
	common.subscreen_timer_handler = timer_tick
	common.draw_background()
	common.pguapp.init(t, common.screen)

def hide():
	common.subscreen_event_handler = None
	common.subscreen_timer_handler = None

	import mainmenu
	mainmenu.show()
