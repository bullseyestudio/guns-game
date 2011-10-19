
class Waypoint:
	def __init__(self, id, pos, name):
		self.title = name
		self.position = pos
		self.id = id
		self.owner = None

all = []

def by_id(id):
	global all

	for wp in all:
		if wp.id == id:
			return wp
