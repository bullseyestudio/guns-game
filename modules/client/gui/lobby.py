from modules.client.gui import common
from modules.pgu import gui as pgui

teamcount = 2
teams = []

def addPlayer(name,t=1):
	t=t-1
	teams[t].add(name)

def removePlayer(name,t=1):
	t=t-1
	teams[t].remove(name)

wid = common.screen.get_width()
hgt = common.screen.get_height()

t = pgui.Table(width=wid, height=hgt)

t.tr()
t.td(pgui.Spacer(width=150, height=20),colspan=teamcount)

t.tr()

for i in range(teamcount):
	tlist = pgui.List(title='Team {0}'.format(i+1), length='5', width=int(wid/teamcount), height=int(hgt/2))
	teams.append(tlist)
	t.td(teams[i])

t.tr()
cancel_btn = pgui.Button('Cancel', height=40)
cancel_btn.connect(pgui.CLICK, common.show_mpmenu)
t.td(cancel_btn,colspan=teamcount)

t.tr()
t.td(pgui.Spacer(width=150, height=80),colspan=2)