""" Hull shape class. """

from .. import constants

from ..base import base_shape
import hulltypes

class hull_shape(base_shape):
	hover = False

	def __init__(self, type, position, size, hover=False):
		if type not in hulltypes.allowed_types:
			raise ValueError('Unknown hull type ' + str(type))

		base_shape.__init__(self, type, position, size, constants.hull_layer)

		self.hover = hover


