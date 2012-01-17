import pygame
from modules.client.gui import common
from modules.pgu import gui as pgui

hgt = common.screen.get_height()
t = pgui.Table(width=common.screen.get_width(), height=hgt)

t.tr()
t.td(pgui.Image('data/GunsLogo.png', valign=-1), height=int(hgt/2), colspan=2)

t.tr()
turrbtn = pgui.Button('Demo: tracking turrets', width=150, height=30)
t.td(turrbtn)
bgbtn = pgui.Button('Demo: scrolling background', width=150, height=30)
t.td(bgbtn)

t.tr()
mpbtn = pgui.Button('Multiplayer', width=150, height=30)
t.td(mpbtn, colspan=2)

t.tr()
optsbtn = pgui.Button('Options', width=150, height=30)
t.td(optsbtn, colspan=2)

t.tr()
quitbtn = pgui.Button('Quit', width=150, height=30)
t.td(quitbtn, colspan=2)

t.tr()
t.td(pgui.Spacer(width=150, height=int(hgt/2) - (4 * 40)), colspan=2)

initialized = False
def init():
	global initialized
	if initialized:
		return

	global turrbtn, bgbtn,  mpbtn,  optsbtn, quitbtn
	import turrets, bgdemo, mpmenu, optsmenu

	turrbtn.connect(pgui.CLICK, turrets.show)
	bgbtn.connect(pgui.CLICK, bgdemo.show)
	mpbtn.connect(pgui.CLICK, mpmenu.show)
	optsbtn.connect(pgui.CLICK, optsmenu.show)
	quitbtn.connect(pgui.CLICK, quit_handler)

	initialized = True

def show():
	init()

	common.draw_background()
	common.pguapp.init(t, common.screen)

def quit_handler():
	pygame.event.post(pygame.event.Event(pygame.QUIT))
