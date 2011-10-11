""" Basic gun shape file """

from ..base import base_shape
import constants

class gun_shape(base_shape):
	def __init__(self, type, position, layer=1):
		if type not in constants.allowed_types:
			raise ValueError('Unknown gun type ' + str(type))

		base_shape.__init__(self, type, position, constants.sizes[type], layer)
