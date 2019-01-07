import scene
import win
import tcod
import gameinput

class TitleScene(scene.Scene):

	def __init__(self):
		super().__init__()
		self.win = win.Window(0,0,win.screenwidth,win.screenheight)
		self.id = "Title Scene"
		gameinput.registerhandler(self.id,' ',scene.handleexit,None)
		gameinput.registerhandler(self.id,gameinput.KEY_ESCAPE,scene.handlequit,None)
		gameinput.registerhandler(self.id,gameinput.KEY_ENTER,scene.handletogglefullscreen,gameinput.ModeFlags.ALT)

def registerhandler(modename,key,fn,exdata,metaflags):

	def update(self):
		super().update()
		self.win.clear()
		self.win.print(10,10,"Press space to begin!")
		self.win.render()
