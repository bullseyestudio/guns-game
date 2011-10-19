width = 2048
height = 1152
spawn = ( width/2, height/2 )

class PlayerAmbiguityError(Exception):
	def __init__(self, p_one, p_two):
		Exception.__init__(self)

		self.p_one = p_one
		self.p_two = p_two
