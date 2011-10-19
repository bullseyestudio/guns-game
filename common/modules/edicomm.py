
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

		if len(parsed_parts) == 1:
			new_parts.append(parsed_parts[0])
		else:
			new_parts.append(parsed_parts)

	return new_parts

def encode(*stuff):
	"""Encode components into a proper EDIComm string.

	The proper look for the parameters is:
		edicomm.encode("TLA", "parameter", ["list", "parameter"], ('tuples are', 'also okay'))
	Which should create the EDIComm string:
		"TLA parameter list,parameter tuples\ are,also\ okay"
	"""

	ret = ''

	for i in stuff:
		if isinstance(i, basestring):
			i = i.replace(',', '\\,')
			ret += i.replace(' ', '\\ ') + ' '
		elif hasattr(i, '__iter__'):
			lstr = ''

			for x in i:
				if isinstance(x, basestring):
					x = x.replace(',', '\\,')
					x = x.replace(' ', '\\ ')

				lstr += str(x) + ','

			lstr = lstr.rstrip(',')
			ret += lstr + ' '
		elif i == None:
			pass # --Gandalf
		else:
			ret += str(i) + ' '

	ret = ret.rstrip(' ')

	return ret

class EDIException(Exception):
	def __init__(self, id, msg):
		Exception.__init__(self)
		self.id = id
		self.msg = msg
