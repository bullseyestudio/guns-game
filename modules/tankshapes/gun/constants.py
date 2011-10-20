""" Define some quick-accessible aliases for gun-related stuff """

from .. import constants as globals

cannon = globals.id_gun_cannon

sizes = {
	cannon: (8,32)
}

anchors = {
	cannon: (0,24,8,32)
}

allowed_types = sizes.keys()
