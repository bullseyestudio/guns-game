
"""Defines functions to help the Guns! server and client speak to each other.

TODO: More docstringy stuff goes here.
"""

def decode(what):
	"""Decode a EDIComm string into its component parts (splitting lists as needed)"""

	parts = what.split(' ')
	new_parts = []

	# First expansion: each separate parameter, keeping lists together.
	this_part = ''
	for part in parts:
		this_part += part

		merge = part.endswith('\\')

		if merge:
			this_part = this_part[:-1] + ' '
		else:
			new_parts.append(this_part)
			this_part = ''

	parts = new_parts
	new_parts = []

	# Second expansion: lists.
	for part in parts:
		if part.find(',') == -1:
			new_parts.append(part)
			continue

		part_parts = part.split(',')

		parsed_parts = []
		parsed = ''
		for p in part_parts:
			parsed += p

			merge = p.endswith('\\')

			if merge:
				parsed = parsed[:-1] + ','
			else:
				parsed_parts.append(parsed)
				parsed = ''

		new_parts.append(parsed_parts)

	return new_parts

def encode(stuff):
	"""Encode components into a proper EDIComm string.

	The proper look for the "stuff" parameter is:
		["TLA", "parameter", ["list", "parameter"], "another parameter"]
	Which should create the EDIComm string:
		"TLA parameter list,parameter another\ parameter"
	"""
	pass