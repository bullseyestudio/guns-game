""" Demo for tracking turrets """

import pygame
from modules.client.gui import common
from modules.client.gui.shapes import turret, bullet
from modules.pgu import gui as pgui
from modules.client import config

wid = common.screen.get_width()
hgt = common.screen.get_height()

t = pgui.Table(width=wid, height=hgt)

t.tr()
t.td(pgui.Spacer(width=150, height=int(hgt) - 120), colspan=2)

t.tr()
backbtn = pgui.Button('Back to Main Menu', width=150, height=30)
backbtn.connect(pgui.CLICK, common.show_mainmenu)
t.td(backbtn)

t.tr()
t.td(pgui.Spacer(width=150, height=80), colspan=2)

turr = turret.Turret(common.screen, (128,128))
turr2 = turret.Turret(common.screen, (530,255))


shooting = False
def draw_turrets(ev):
	global shooting

	if(ev.type == config.TIMER_EVENT):
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
	elif(ev.type == pygame.MOUSEMOTION):
		turr.point_at(ev.pos)
		turr2.point_at(ev.pos)
	elif(ev.type == pygame.MOUSEBUTTONDOWN):
		if(backbtn.is_hovering()):
			return

		shooting = True
	elif(ev.type == pygame.MOUSEBUTTONUP) and shooting:
		shooting = False
