""" Demo for tracking turrets """

import pygame
from modules.client.gui import common
from modules.client.gui.shapes import turret
from modules.pgu import gui as pgui

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

def draw_turrets(ev):
	if(ev.type != pygame.MOUSEMOTION):
		return

	turr.point_at(ev.pos)
	rect = turr.paint()
	pygame.display.update(rect)

	turr2.point_at(ev.pos)
	rect = turr2.paint()
	pygame.display.update(rect)
