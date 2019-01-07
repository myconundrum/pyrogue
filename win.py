import tcod



screenwidth 		= 120
screenheight 		= 50
limitfps 			= 60


white = tcod.white
gold = tcod.gold
red = tcod.red



class Window():
	def __init__(self,x,y,width,height):

		self.con = tcod.console_new(width,height)
		self.width = width
		self.height = height
		self.x = x 
		self.y = y

		self.cx = 0
		self.cy = 0

		self.bgalpha = 1.0
		self.fgalpha = 1.0

	def setalpha(self,fg,bg):
		self.fgalpha = fg
		self.bgalpha = bg 

	def getcamrect(self):
		return (self.cx,self.cy,self.width,self.height)

	def tocam(self,x,y):
		return (x-self.cx,y-self.cy)

	def incam(self,x,y):
		return (x >= self.cx and x < self.cx + self.width) and (y>= self.cy and y < self.cy + self.height)

	def setcamera(self,x,y):
		self.cx = max(0,x)
		self.cy = max(0,y)

	def centercam(self,x,y):
		self.setcamera(x - (self.width // 2), y - (self.height // 2))

	def setfg(self,color):
		tcod.console_set_default_foreground(self.con,color)

	def setbg(self,color):
		tcod.console_set_default_background(self.con,color)

	def render(self):
		tcod.console_blit(self.con,0,0,self.width,self.height,root,self.x,self.y,self.fgalpha,self.bgalpha)

	def putchar(self,x,y,rep,color):
		(x,y) = self.tocam(x,y)
		tcod.console_put_char(self.con,x,y,rep)
		tcod.console_set_char_foreground(self.con,x,y,color)


	def putblock(self,x,y,color):
		(x,y) = self.tocam(x,y)
		tcod.console_set_char_background(self.con,x,y,color,tcod.BKGND_SET)

	def print(self,x,y,fmt):
		(x,y) = self.tocam(x,y)
		tcod.console_print(self.con,x,y,fmt)

	def clear(self):
		tcod.console_clear(self.con)

def color(r,g,b):
	return tcod.Color(r,g,b)

def clear():
	tcod.console_clear(root)

def init():

	global root
	tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
	root = tcod.console_init_root(screenwidth, screenheight, 'Test', False)
	tcod.sys_set_fps(limitfps)

def togglefullscreen():
	setfullscreen(isfullscreen())

def setfullscreen(full):
	tcod.console_set_fullscreen(full)

def isfullscreen():
	return tcod.console_is_fullscreen()

def flip():
	tcod.console_flush()


