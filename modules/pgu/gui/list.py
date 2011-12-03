"""
"""
from .const import *
from . import container, widget

class List(container.Container):

	def __init__(self, title=None, length=None, show_empty=True, size=20, **params):
		params.setdefault('cls','list')
		container.Container.__init__(self, **params)

		self.title = title

		self.font = self.style.font

		w,h = self.font.size("e"*size)
		self.size = size
		self.style.width = w + ( self.style.padding * 2) + 8

		self.itmheight = h
		self.itmwidth = w
		self.vpos = 0

		self.cls = params['cls']

		self.padding = self.style.padding
		self.offset = 0
		if self.title != None:
			tw,th = self.font.size(self.title)
			self.offset += th + 10

	def add(self,name):
		itm = ListItem(value=name,cls='{0}.item'.format(self.cls),size=self.size)
		container.Container.add(self,itm,self.padding,self.padding+self.offset)
		container.Container.repaint(self)
		self.offset += self.itmheight

	def remove(self,name):
		for itm in self.widgets:
			if itm.get_text() == name:
				container.Container.remove(self,itm)
				container.Container.repaint(self)
				self.offset -= self.itmheight

	def paint(self,s):
		if self.title != None:
			# Painting the title...
			tw,th = self.font.size(self.title)
			s.blit(self.font.render(self.title, 1, self.style.color),((self.style.width/2) - (tw/2),0))

		container.Container.paint(self,s)

#	def paint(self,s):
#		container.Container.paint(self,s)
#			r = pygame.Rect(0,offset,self.rect.w,self.rect.h)
#
#			cs = 2 #NOTE: should be in a style
#
#			w,h = self.font.size(item)
#			x = w-self.vpos
#			if x < 0: self.vpos -= -x
#			if x+cs > s.get_width(): self.vpos += x+cs-s.get_width()

#			s.blit(self.font.render(item, 1, self.style.color),(-self.vpos + self.padding,offset))
#			count += 1
#			offset += self.height+self.padding

class ListItem(widget.Widget):
	def __init__(self, value='', **params):

		cls = None
		if 'cls' in params:
			cls = params['cls']
		else:
			cls = 'list'

		params.setdefault('cls','{0}.item'.format(cls))
		widget.Widget.__init__(self, **params)

		params.setdefault('size',20)
		self.size = params['size']

		self.value = value
		self.pos = len(str(value))
		self.vpos = 0
		self.font = self.style.font
		w,h = self.font.size("e"*self.size)
		if not self.style.height: self.style.height = h
		if not self.style.width: self.style.width = w

	def set_text(self, text):
		self.value = text

	def get_text(self):
		return self.value

	def paint(self,s):
		r = pygame.Rect(0,0,self.rect.w,self.rect.h)

		cs = 2 #NOTE: should be in a style

		w,h = self.font.size(self.value[0:self.pos])
		x = w-self.vpos
		if x < 0: self.vpos -= -x
		if x+cs > s.get_width(): self.vpos += x+cs-s.get_width()

		s.blit(self.font.render(self.value, 1, self.style.color),(-self.vpos,0))