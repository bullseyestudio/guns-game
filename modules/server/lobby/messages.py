import Queue, sys
from modules.server.lobby import player

queue = Queue.Queue()

class Message:
	def __init__(self, addr, data):
		self.addr = addr
		self.data = data

def enqueue(addr, data):
	msg = Message(addr, data)
	queue.put(msg)

def process_queue():
	while(not queue.empty()):
		try:
			msg = queue.get(False)
		except Queue.Empty:
			# Swallow and return; should never happen, but defensive programming ftw.
			return

		p = player.by_addr(msg.addr)

		if not p:
			# We can't process a message from a non-existing player, so just drop it
			# This could happen if player sends "USD reason\nOTHER_MESSAGE\n"
			continue

		p.process_message(msg)
