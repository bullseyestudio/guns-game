import pygame
from modules.client.gui import common
from modules.pgu import gui as pgui

def quit_handler():
	pygame.event.post(pygame.event.Event(pygame.QUIT))

wid = common.screen.get_width()
hgt = common.screen.get_height()

t = pgui.Table(width=wid, height=hgt)

t.tr()
t.td(pgui.Image('data/GunsLogo.png', valign=-1), height=int(hgt/2))

t.tr()
t.td(pgui.Button('Build a tank', width=150, height=30))

t.tr()
t.td(pgui.Button('Multiplayer', width=150, height=30))

t.tr()
optsbtn = pgui.Button('Options', width=150, height=30)
t.td(optsbtn)

t.tr()
b = pgui.Button('Quit', width=150, height=30)
b.connect(pgui.CLICK, quit_handler)
t.td(b)

t.tr()
t.td(pgui.Spacer(width=150, height=int(hgt/2) - (4 * 40)))
