import tcod



screenwidth 		= 120
screenheight 		= 50
limitfps 			= 60


layerworld 	= 0
layerui		= 1
layerhud    = 2
layermodal  = 3




_windows = []



class Window(tcod.console.Console):
	def __init__(self,x,y,width,height,layer=layerworld):
		super().__init__(width,height)
		self.x = x 
		self.y = y
		self._active = False
		self._layer = layer 


	def flush(self):
		self.blit(root,self.x,self.y,0,0,self.width,self.height)





def init():

	global root

	tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
	root = tcod.console_init_root(screenwidth, screenheight, 'Test', False)
	tcod.sys_set_fps(limitfps)


def flip():


	tcod.console_flush()



def main():

	init()

	playing = True
	wina = Window(0,0,10,screenheight)
	winb = Window(0,0,screenwidth,screenheight)
	winc = Window(screenwidth//2,screenheight//2,10,10)



	winb.print_(50,20,"Hello World!")
	winb.print_(0,20,"Here I am!")
	wina.print_(0,0,"Yo Yo Yo")
	winc.print_(10,10,'@@YO@@')
	for y in range(winc.height):
		for x in range(winc.width):
			tcod.console_set_char_background(winc,x,y,tcod.Color(20,20,20),tcod.BKGND_SET)


	while not tcod.console_is_window_closed() and playing:

		root.clear()
		winb.flush()
		wina.flush()
		winc.flush()
		flip()
		key = tcod.console_wait_for_keypress(True)

		if key.vk == tcod.KEY_ENTER and key.lalt:
			# Alt+Enter: toggle fullscreen
			tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
		
		elif key.vk == tcod.KEY_ESCAPE:
			playing = False
			return
		if tcod.console_is_key_pressed(tcod.KEY_UP):
			winc.y -=1
		elif tcod.console_is_key_pressed(tcod.KEY_DOWN):
			winc.y +=1
		elif tcod.console_is_key_pressed(tcod.KEY_LEFT):
			winc.x -=1
		elif tcod.console_is_key_pressed(tcod.KEY_RIGHT):
			winc.x +=1






main()

