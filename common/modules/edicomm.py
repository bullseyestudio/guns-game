
"""Defines functions to help the Guns! server and client speak to each other.

TODO: More docstringy stuff goes here.
"""

def decode(what):
	"""Decode a EDIComm string into its component parts (splitting lists as needed)"""
	pass

def encode(stuff):
	"""Encode components into a proper EDIComm string.

	The proper look for the "stuff" parameter is:
		["TLA", "parameter", ["list", "parameter"], "another parameter"]
	Which should create the EDIComm string:
		"TLA parameter list,parameter another\ parameter"
	"""
	pass
