""" Base tank shape -- all other shapes derive from this

Minimal requirements:
- typeID
- position (relative to tank origin)
- size (fixed for most shapes)
- layer (fixed for most shapes)

"""

class base_shape(object):
	type = 0
	position = (0,0)
	size = (0,0)
	layer = 0

	def __init__(self, type, position, size, layer=0):
		# TODO: Don't forget to do some kind of validation!
		self.type = type
		self.position = position
		self.size = size
		self.layer = layer
	
