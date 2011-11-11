from modules.client.gui import common
from modules.pgu import gui as pgui

wid = common.screen.get_width()
hgt = common.screen.get_height()

t = pgui.Table(width=wid, height=hgt)

t.tr()
t.td(pgui.Spacer(width=150, height=int(hgt/2) - (2 * 40)), colspan=2)

t.tr()
t.td(pgui.Label('Nothing to report today, Judd!', height=30), colspan=2)

t.tr()
t.td(pgui.Spacer(width=150, height=int(hgt/2) - (4 * 40)), colspan=2)

t.tr()
backbtn = pgui.Button('Back to Main Menu', width=150, height=30)
t.td(backbtn)
savebtn = pgui.Button('Save Settings', width=150, height=30)
t.td(savebtn)

t.tr()
t.td(pgui.Spacer(width=150, height=80), colspan=2)
