""" Base tank shape -- all other shapes derive from this

Minimal requirements:
- typeID
- position (relative to tank origin)
- size (fixed for most shapes)
- layer (fixed for most shapes)
- anchor rectangle (what portion of the shape must be supported by the lower layer;
	most shapes will define their entire extent as their anchor rectangle)

"""

class base_shape(object):
	type = 0
	position = (0,0)
	size = (0,0)
	anchor = (0,0)
	layer = 0

	def __init__(self, type, position, size, layer=0, anchor=None):
		# TODO: Don't forget to do some kind of validation!
		self.type = type
		self.position = position
		self.size = size
		self.layer = layer

		if anchor:
			self.anchor = anchor
		else:
			self.anchor = (0,0) + size

	def absanchor(self):
		""" Returns the anchor rectangle relative to the tank origin (i.e. NOT relative to the shape) """
		return self.position + (self.position[0]+self.anchor[2], self.position[1]+self.anchor[3])

	def __repr__(self):
		return '<shape(type={self.type})>'.format(self=self)

	def __str__(self):
		return '{0}(type={self.type},position={self.position},size={self.size},layer={self.layer},anchor={self.anchor})'.format(
			type(self),
			self=self)
