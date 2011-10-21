""" Hull shape class. """

from .. import constants as globals

from ..base import base_shape
import constants

class hull_shape(base_shape):
	hover = False

	def __init__(self, type, position, size, hover=False):
		if type not in constants.allowed_types:
			raise ValueError('Unknown hull type ' + str(type))

		base_shape.__init__(self, type, position, size, globals.layer_hull)

		self.hover = hover


